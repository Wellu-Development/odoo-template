from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

class NenaL10NTaxUnit(models.Model):
    _name = 'nena.l10n.ve.tax.unit'
    _description = 'SENIAT Tax Unit (UT) Value'
    _order = 'effective_date desc'
    _rec_name = 'effective_date'

    # --- Model Fields ---

    name = fields.Char(
        string='Reference',
        required=True,
        default='Tax Unit'
    )

    value = fields.Float(
        string='Value (Bs.)',
        digits=(10, 2),
        required=True
    )

    effective_date = fields.Date(
        string='Effective Date',
        required=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    is_current = fields.Boolean(
        string='Is Current',
        compute='_compute_is_current',
        store=True,
        help='Indicates if this is the currently effective UT value for the company.'
    )

    # --- Constraints ---

    _sql_constraints = [
        ('date_company_uniq', 'unique (effective_date, company_id)',
         'A Tax Unit value already exists for this date and company.')
    ]

    # --- Compute Methods ---

    @api.depends('effective_date', 'company_id')
    def _compute_is_current(self):
        for record in self:
            current_ut = self.search([
                ('company_id', '=', record.company_id.id)
            ], order='effective_date desc', limit=1)
            record.is_current = (record.id == current_ut.id)

    # --- Utility Method ---

    @api.model
    def get_value_for_date(self, check_date=None, company_id=None):
        """Get UT value effective on or before the given date for the given company."""
        if not check_date:
            check_date = date.today()
        if not company_id:
            company_id = self.env.company.id

        ut_record = self.search([
            ('effective_date', '<=', check_date),
            ('company_id', '=', company_id)
        ], order='effective_date desc', limit=1)

        if not ut_record:
            raise UserError("No Tax Unit value has been configured for this date and company.")

        return ut_record.value