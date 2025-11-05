from lxml import etree
from odoo import _, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    """
    Documentation for Swiss ISO20022 on:
    https://www.six-group.com/dam/download/banking-services/standardization/sps/ig-credit-transfer-sps2024-2.1.1-en.pdf
    """

    _inherit = "account.journal"

    def get_document_namespace(self, payment_method_code):
        if payment_method_code == 'iso20022_ch':
            return 'http://www.six-interbank-clearing.com/de/pain.001.001.03.ch.02.xsd'
        return super().get_document_namespace(payment_method_code)

    def _get_Dbtr(self, payment_method_code):
        Dbtr = super()._get_Dbtr(payment_method_code)
        if payment_method_code == 'iso20022_ch':
            result = list(filter(lambda x: x.tag != 'Id', Dbtr))
            new_dbtr = etree.Element('Dbtr')
            new_dbtr.extend(result)
            return new_dbtr
        return Dbtr

    def _get_PmtTpInf(self, payment_method_code):
        if payment_method_code == 'iso20022_ch':
            return etree.Element("PmtTpInf")
        return super()._get_PmtTpInf(payment_method_code)

    def _get_group_payment_method_code(self, payment_method_code, currency_id):
        # EXTENDS account_iso20022
        group_payment_method_code = super()._get_group_payment_method_code(payment_method_code, currency_id)
        if payment_method_code == 'iso20022_ch':
            if currency_id == self.env.ref('base.EUR').id:
                group_payment_method_code = 'sepa_ct'
            elif currency_id != self.env.ref('base.CHF').id:
                group_payment_method_code = 'iso20022'
        return group_payment_method_code

    def _get_cleaned_bic_code(self, bank_account, payment_method_code):
        bic_code = super()._get_cleaned_bic_code(bank_account, payment_method_code)
        if payment_method_code == 'iso20022_ch' and bic_code is None:
            if not bank_account:
                raise UserError(_(
                    "Please set an account number on the journal '%(journal_name)s'.",
                    journal_name=self.name,
                ))
            if not bank_account.bank_id:
                raise UserError(_(
                    "Please set a bank on the journal '%(journal_name)s'.",
                    journal_name=self.name,
                ))
            raise UserError(_(
                "Please set the bank identifier code (BIC) on this bank: %(bank_name)s",
                bank_name=bank_account.bank_id.name,
            ))
        return bic_code
