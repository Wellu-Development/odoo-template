from lxml import etree

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.depends('bank_acc_number', 'company_id.account_fiscal_country_id', 'company_id.country_id')
    def _compute_sepa_pain_version(self):
        se_bban_journals = self.filtered(lambda j: j.bank_account_id.acc_type in ('bban_se', 'plusgiro', 'bankgiro'))
        # For SE BBAN, we use the pain.001.001.03 version
        se_bban_journals.sepa_pain_version = 'pain.001.001.03'
        super(AccountJournal, self - se_bban_journals)._compute_sepa_pain_version()

    def _is_se_bban(self, payment_method_code, partner_acc_type=None):
        """ Whenever this journal should be considered as a swedish bban, plusgiro or bankgiro
            in a batch payment.

            :param payment_method_code: The payment method used for the payment
            :param partner_acc_type: A set containing the different acc_type of all the payments
                                     we want to add in the xml file.

            :return: True if the payment method is set to **iso20022_se** and either the bank account
                     is not IBAN or there is any IBAN payments, else False.
        """
        return (
            payment_method_code == 'iso20022_se'
            and (
                self.bank_account_id.acc_type in {'bban_se', 'plusgiro', 'bankgiro'}
                or len({'bban_se', 'plusgiro', 'bankgiro', *(partner_acc_type or {'iban'})}) == 3
            )
        )

    def _get_CtgyPurp(self, payment_method_code):
        if not self._is_se_bban(payment_method_code):
            return super()._get_CtgyPurp(payment_method_code)

        CtgyPurp = etree.Element('CtgyPurp')
        Cd = etree.SubElement(CtgyPurp, 'Cd')
        Cd.text = 'SALA' if self.env.context.get('sepa_payroll_sala') else 'SUPP'
        return CtgyPurp

    def _get_DbtrAcct(self, payment_method_code=None, payments=None):
        # EXTEND of account_iso20022
        payments = payments or []
        acc_types = {payment['acc_type'] for payment in payments}
        if payment_method_code != 'iso20022_se' or 'iban' in acc_types:
            return super()._get_DbtrAcct(payment_method_code, payments)

        if not self.bank_account_id.sanitized_acc_number:
            raise UserError(_("This journal does not have a bank account defined."))
        DbtrAcct = etree.Element("DbtrAcct")
        Id = etree.SubElement(DbtrAcct, "Id")
        Id.append(self._get_DbtrAcctOthr(payment_method_code, acc_types))
        Ccy = etree.SubElement(DbtrAcct, "Ccy")
        Ccy.text = self.currency_id.name or self.company_id.currency_id.name
        return DbtrAcct

    def _get_DbtrAcctOthr(self, payment_method_code=None, partner_acc_type=None):
        # EXTEND of account_iso20022
        if not self._is_se_bban(payment_method_code, partner_acc_type):
            return super()._get_DbtrAcctOthr(payment_method_code, partner_acc_type)

        Othr = etree.Element("Othr")
        OthrId = etree.SubElement(Othr, "Id")
        if self.bank_account_id.sanitized_acc_number.isdigit():
            OthrId.text = self.bank_account_id.sanitized_acc_number
        else:
            bank_code, account_number, _checksum = self.bank_account_id._se_get_acc_number_data(self.bank_account_id.sanitized_acc_number)
            OthrId.text = f"{bank_code}{account_number}"
        SchmeNm = etree.SubElement(Othr, "SchmeNm")
        if self.bank_account_id.acc_type == 'bankgiro':
            Prtry = etree.SubElement(SchmeNm, "Prtry")
            Prtry.text = 'BGNR'
        else:
            Cd = etree.SubElement(SchmeNm, "Cd")
            Cd.text = 'BBAN'
        return Othr

    def _get_CdtrAcctIdOthr(self, bank_account, payment_method_code=None):
        if not self._is_se_bban(payment_method_code):
            return super()._get_CdtrAcctIdOthr(bank_account, payment_method_code)

        Othr = etree.Element("Othr")
        Id = etree.SubElement(Othr, "Id")
        Id.text = bank_account.sanitized_acc_number
        SchmeNm = etree.SubElement(Othr, "SchmeNm")
        if bank_account.acc_type == 'bankgiro':
            Prtry = etree.SubElement(SchmeNm, "Prtry")
            Prtry.text = 'BGNR'
        else:
            Cd = etree.SubElement(SchmeNm, "Cd")
            Cd.text = 'BBAN'
        return Othr

    def _get_FinInstnId(self, bank_account, payment_method_code):
        if not self._is_se_bban(payment_method_code):
            return super()._get_FinInstnId(bank_account, payment_method_code)

        FinInstnId = etree.Element("FinInstnId")
        ClrSysMmbId = etree.SubElement(FinInstnId, "ClrSysMmbId")
        ClrSysId = etree.SubElement(ClrSysMmbId, "ClrSysId")
        Cd = etree.SubElement(ClrSysId, "Cd")
        Cd.text = "SESBA"
        MmbId = etree.SubElement(ClrSysMmbId, "MmbId")
        if bank_account.acc_type == 'bankgiro':
            MmbId.text = '9900'
        elif bank_account.acc_type == 'plusgiro':
            MmbId.text = '9500'
        else:
            bank_code, _acc_num, _checksum = bank_account._se_get_acc_number_data(bank_account.acc_number)
            MmbId.text = bank_code[:4]
        return FinInstnId

    def _get_cleaned_bic_code(self, bank_account, payment_method_code):
        """
        Return the cleaned or hardcoded BIC code for the given bank account.

        This override handles Swedish-specific account types for SEPA payments:
        - Bankgiro accounts return 'SE:Bankgiro'
        - Plusgiro accounts return 'SE:Plusgiro'

        For all other account types and countries, the method falls back to the
        standard implementation.

        :param bank_account: The bank account record to retrieve the BIC for.
        :type bank_account: res.partner.bank
        :param payment_method_code: The payment method code, e.g., 'iso20022_se'.
        :type payment_method_code: str
        :return: The cleaned BIC code or a hardcoded SE-specific BIC.
        :rtype: str
        """
        if payment_method_code == 'iso20022_se' and bank_account.acc_type in ('plusgiro', 'bankgiro'):
            return 'SE:Bankgiro' if bank_account.acc_type == 'bankgiro' else 'SE:Plusgiro'
        return super()._get_cleaned_bic_code(bank_account, payment_method_code)

    def _skip_CdtrAgt(self, partner_bank, payment_method_code):
        """
        Determine whether to skip the Creditor Agent (CdtrAgt) element in SEPA XML.

        This override ensures that for Swedish Bankgiro and Plusgiro accounts,
        the CdtrAgt element is always included, even if the BIC is missing.

        For other accounts or payment methods, the standard behavior is preserved.

        :param partner_bank: The partner's bank account record.
        :type partner_bank: res.partner.bank
        :param payment_method_code: The payment method code, e.g., 'iso20022_se'.
        :type payment_method_code: str
        :return: False to indicate that CdtrAgt should not be skipped, or the
                 result of the standard implementation.
        :rtype: bool
        """
        if payment_method_code == 'iso20022_se' and partner_bank.acc_type in ('bankgiro', 'plusgiro'):
            return False
        return super()._skip_CdtrAgt(partner_bank, payment_method_code)
