from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

class NenaL10nVETaxRetention(models.Model):
    # Se recomienda cambiar el nombre del modelo a l10n_ve.tax.retention
    _name = 'nena.l10n.ve.tax.retention' 
    _description = 'SENIAT IVA Tax Retention Rates History'
    _order = 'start_date desc'

    name = fields.Char(
        string='Reference',
        required=True,
        default='IVA Retention Rate Configuration'
    )
    
    # 🌟 CORRECCIÓN CRÍTICA: Campo para distinguir la regla (Estándar vs. Penalidad)
    retention_type = fields.Selection([
        ('standard', 'Standard'),
        ('penalty', 'Penalty Rate (100%)'),
    ], string='Retention Type', required=True, default='standard',
       help="Distinguishes the fiscal rule this rate applies to.")

    rate = fields.Float(
        string='Retention Rate (%)',
        digits=(10, 2),
        required=True
    )

    start_date = fields.Date(
        string='Start Date',
        required=True
    )

    end_date = fields.Date(
        string='End Date',
        help='Leave blank if the rate is still valid.'
    )

    is_current = fields.Boolean(
        string='Is Current',
        compute='_compute_is_current',
        store=True,
        help='Indicates if this rate is currently effective.'
    )

    # --- Model Methods ---

    @api.depends('start_date', 'end_date')
    def _compute_is_current(self):
        # Finds the current retention rate for each type
        today = date.today()
        for record in self:
            record.is_current = (record.start_date and record.start_date <= today and (not record.end_date or record.end_date >= today))

    @api.model
    def get_rate_for_date(self, check_date=None, retention_type='standard'):
        """
        Busca el valor de la tasa (float) vigente para una fecha específica y un TIPO de retención.
        
        :param retention_type: 'standard' o 'penalty'.
        :return: El valor de la tasa como float (ej: 75.00).
        """
        if not check_date:
            check_date = date.today()

        # 🌟 Se incluye el filtro 'retention_type' en el domain
        domain = [
            ('start_date', '<=', check_date),
            ('retention_type', '=', retention_type), # <--- FILTRO CRÍTICO
            '|',
            ('end_date', '>=', check_date),
            ('end_date', '=', False)
        ]
        
        # Busca el registro más reciente que cumpla con la fecha y el tipo.
        rate_record = self.search(domain, order='start_date desc', limit=1)

        if not rate_record:
            raise UserError(
                f"Configuration Error: No valid '{retention_type}' Tax Retention rate found for the date {check_date}. "
                "Please configure the rate history."
            )
        
        # 🌟 CORRECCIÓN: Devuelve un solo valor float, no una lista.
        return rate_record.rate