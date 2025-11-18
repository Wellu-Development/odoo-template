from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class ResCompany(models.Model):
    _inherit = 'res.company'

    # 1. Indicador SPE para Compras (Agente de Retención)
    is_special_taxpayer = fields.Boolean(
        string='Is Withholding Agent (SPE)',
        help="Mark if your company is designated as a Sujeto Pasivo Especial (SPE) by SENIAT.",
        default=False
    )

    # 2. Regla de Retención para COMPRAS (Tú retienes a proveedores)
    # Define la regla que TU compañía debe aplicar (e.g., standard 75% or penalty 100%).
    # Esto se usa en account.move para calcular la retención.
    iva_purchase_retention_rule_id = fields.Many2one(
        'l10n_ve.tax.retention',
        string='IVA Withholding Rule (Purchases)',
        domain="[('end_date', '=', False), ('retention_type', 'in', ['standard', 'penalty'])]",
        help="The IVA withholding rule your company applies to its suppliers."
    )

    # 3. Regla de Retención para VENTAS (El cliente te retiene a ti)
    # Define la regla que TU compañía ESPERA que le aplique un cliente SPE.
    # Esto se usa para calcular el monto esperado de descuento en la cobranza.
    iva_sales_retention_rule_id = fields.Many2one(
        'l10n_ve.tax.retention',
        string='IVA Withholding Rule (Sales)',
        domain="[('end_date', '=', False), ('retention_type', 'in', ['standard', 'penalty'])]",
        help="The IVA withholding rule your company expects customers to apply."
    )

    # Campo calculado para visualizar la tasa vigente de la regla de compras
    current_iva_purchase_rate = fields.Float(
        string='Current Purchase Rate (%)',
        compute='_compute_current_iva_rate',
        help='Shows the current effective IVA purchase retention rate for the selected rule.',
        store=False 
    )

    @api.depends('iva_purchase_retention_rule_id')
    def _compute_current_iva_rate(self):
        """Retrieves the current rate value from the historical configuration."""
        today = fields.Date.today()
        retention_model = self.env['l10n_ve.tax.retention']
        
        for company in self:
            company.current_iva_purchase_rate = 0.0
            
            if company.iva_purchase_retention_rule_id:
                try:
                    rate_type = company.iva_purchase_retention_rule_id.retention_type
                    
                    company.current_iva_purchase_rate = retention_model.get_rate_for_date(
                        check_date=today,
                        retention_type=rate_type
                    )
                except UserError:
                    # If rate is not found, leave at 0.0 and let the full calculation raise the error
                    pass