from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

class L10nVETaxUnit(models.Model):
    # Technical name of the model (usually in 'l10n_ve.model_name' format)
    _name = 'l10n_ve.tax.unit'
    _description = 'SENIAT Tax Unit (UT) Value'
    # Orders the records by effective date descending to easily find the current value
    _order = 'effective_date desc'

    # --- Model Fields ---

    name = fields.Char(
        string='Reference',
        required=True,
        default='Tax Unit'
    )
    # Field to store the monetary value of the UT (Bs. 43.00)
    value = fields.Float(
        string='Value (Bs.)',
        digits=(10, 2),  # Allows up to 2 decimal places
        required=True
    )
    # Field to register the date on which the UT value becomes effective
    effective_date = fields.Date(
        string='Effective Date',
        required=True
    )
    # Computed field to identify if this record holds the currently effective value
    is_current = fields.Boolean(
        string='Is Current',
        compute='_compute_is_current',
        store=True,
        help='Indicates if this is the currently effective UT value.'
    )

    # --- Model Methods ---

    # 1. Method to compute if a record is the current value
    @api.depends('effective_date')
    def _compute_is_current(self):
        # Finds the UT with the most recent effective date
        current_ut = self.search([], order='effective_date desc', limit=1)
        for record in self:
            record.is_current = (record == current_ut)

    # 2. SQL Constraint to prevent duplicate effective dates
    _sql_constraints = [
        ('date_uniq', 'unique (effective_date)',
         'A Tax Unit value already exists with this effective date.')
    ]

    # 3. Method to retrieve the UT value for a specific date (CRUCIAL!)
    @api.model
    def get_value_for_date(self, check_date=None):
        """
        Searches for the effective UT value on or before the specified date.
        :param check_date: Date to check against. Defaults to today's date.
        :return: The UT value (float).
        """
        if not check_date:
            check_date = date.today()

        # Searches for the UT value whose effective date is less than or equal to the check date,
        # and which is the most recent (desc).
        ut_record = self.search([('effective_date', '<=', check_date)],
                                order='effective_date desc', limit=1)

        if not ut_record:
            # If no records exist (initial case)
            raise UserError("No value has been configured for the Tax Unit (UT).")
            
        return ut_record.value