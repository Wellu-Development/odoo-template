from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campos de retención comunes para compras y ventas
    iva_retention_rate = fields.Float(
        string='Applied IVA Rate (%)',
        digits=(10, 2),
        readonly=True,
        copy=False,
        help="The actual percentage applied or expected to be applied (e.g., 75.00)."
    )

    iva_retention_amount = fields.Monetary(
        string='IVA Withholding Amount',
        readonly=True,
        copy=False,
        currency_field='company_currency_id',
        help="The total amount withheld or expected to be withheld."
    )
    
    iva_retention_processed = fields.Boolean(
        string='IVA Processed',
        copy=False,
        default=False
    )
    
    # -------------------------------------------------------------------------
    # Overriding action_post to trigger calculation BEFORE the move is posted
    # -------------------------------------------------------------------------

    def action_post(self):
        """
        Overrides action_post to calculate and register the IVA withholding before posting.
        """
        # Calculate/register the IVA retention for this document
        self._l10n_ve_calculate_and_register_iva_retention()
        
        # Call the original Odoo method to complete posting
        return super(AccountMove, self).action_post()

    def _l10n_ve_calculate_and_register_iva_retention(self):
        """
        Determines the role (Agent or Subject) and calls the appropriate function.
        """
        if self.iva_retention_processed or self.move_type not in ('in_invoice', 'out_invoice'):
            return

        is_purchase = self.move_type == 'in_invoice'
        is_agent = self.company_id.is_special_taxpayer 

        # Case A: Purchase (In-Invoice). My company is the AGENT and MUST withhold.
        if is_agent and is_purchase:
            self._l10n_ve_process_purchase_withholding()
        
        # Case B: Sale (Out-Invoice). The Partner (Client) is the AGENT and withholds from us.
        elif self.partner_id.is_special_taxpayer and not is_purchase:
            self._l10n_ve_register_expected_sales_withholding()
        
        # Mark as processed to prevent recalculation
        self.iva_retention_processed = True


    # -------------------------------------------------------------------------
    # Logic for Purchase Invoices (My Company Withholds)
    # -------------------------------------------------------------------------
    
    def _l10n_ve_process_purchase_withholding(self):
        """Calculates and registers the withholding applied to a supplier (Purchase Bill)."""
        
        # 1. Get the Rule from the Supplier (Partner)
        partner_rule = self.partner_id.iva_purchase_retention_rule_id 

        if not partner_rule:
             # The system should prevent posting if the rule is missing and the company is SPE
            raise UserError(
                _("Configuration Error: Missing 'IVA Withholding Rule (Purchases)' on supplier '%s'.") 
                % self.partner_id.display_name
            )
        
        # 2. Search for the effective rate value (e.g., 75.00)
        check_date = self.date or date.today()
        retention_model = self.env['l10n_ve.tax.retention']
        
        retention_rate_percentage = retention_model.get_rate_for_date(
            check_date=check_date, 
            retention_type=partner_rule.retention_type # Uses 'standard' or 'penalty' from Partner config
        )
        
        # 3. Calculate Withholding Amount
        iva_tax_amount = sum(line.tax_base_amount for line in self.line_ids.filtered(lambda l: l.tax_line_id and 'IVA' in l.tax_line_id.name))
        
        if iva_tax_amount <= 0.0:
            return

        retention_rate = retention_rate_percentage / 100.0
        retention_amount = iva_tax_amount * retention_rate
        
        # 4. Save Amount and Rate
        self.write({
            'iva_retention_rate': retention_rate_percentage,
            'iva_retention_amount': retention_amount,
        })
        
        # 5. ⚠️ Placeholder for Accounting Entry Creation (CRITICAL)
        # This is where the actual journal item for the payable liability is created,
        # reducing the amount owed to the supplier (account.move.line creation logic goes here).
        
        return True # Indicates successful processing


    # -------------------------------------------------------------------------
    # Logic for Sales Invoices (Client Withholds from My Company)
    # -------------------------------------------------------------------------

    def _l10n_ve_register_expected_sales_withholding(self):
        """Registers the expected withholding amount applied by the client (Sales Invoice)."""

        # 1. Get the Rule from My Company
        company_rule = self.company_id.iva_sales_retention_rule_id 

        if not company_rule:
            # We don't raise an error, but we cannot calculate the expected amount
            return

        # 2. Search for the expected effective rate value
        check_date = self.date or date.today()
        retention_model = self.env['l10n_ve.tax.retention']
        
        retention_rate_percentage = retention_model.get_rate_for_date(
            check_date=check_date, 
            retention_type=company_rule.retention_type
        )
        
        # 3. Calculate Expected Withholding Amount
        iva_tax_amount = self.amount_tax
        
        retention_rate = retention_rate_percentage / 100.0
        expected_retention_amount = iva_tax_amount * retention_rate
        
        # 4. Save Expected Amount and Rate
        self.write({
            'iva_retention_rate': retention_rate_percentage,
            'iva_retention_amount': expected_retention_amount,
        })
        
        # 5. ⚠️ Logic to record the Receivable Asset (Actual asset creation and
        # reduction of the Account Receivable is usually done during payment/reconciliation).
        
        return True