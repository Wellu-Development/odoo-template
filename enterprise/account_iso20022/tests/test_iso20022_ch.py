from odoo.addons.account_iso20022.tests.test_iso20022_common import TestISO20022CommonCreditTransfer
from odoo.models import Command


class TestISO20022CH(TestISO20022CommonCreditTransfer):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.payment_method = cls.env.ref('account_iso20022.account_payment_method_iso20022_ch')
        cls.swiss_partner = cls.env['res.partner'].create({
            'name': 'Swiss Customer',
            'street': 'Swiss Street',
            'country_id': cls.env.ref('base.ch').id,
        })
        cls.swiss_bank = cls.env['res.bank'].create({
            'name': 'BANK SWITZERLAND',
            'bic': 'BKCHLIWWXXX',
        })
        cls.company_data['default_journal_bank'].update({
            'bank_acc_number': 'CH35 2060 4961 4719 6834',
            'bank_id': cls.swiss_bank.id,
        })
        cls.swiss_partner_bank = cls.env['res.partner.bank'].create({
            'acc_number': 'CH35 2060 4961 4719 6834',
            'allow_out_payment': True,
            'partner_id': cls.swiss_partner.id,
            'acc_type': 'bank',
            'bank_name': cls.swiss_bank.name,
            'bank_id': cls.swiss_bank.id,
        })
        cls.bank_journal = cls.company_data['default_journal_bank']
        cls.payment_method_line = cls.env['account.payment.method.line'].create({
            'journal_id': cls.bank_journal.id,
            'payment_method_id': cls.payment_method.id,
        })

    def test_compliance_with_pain_001_001_09(self):
        """ The XML tree is compliant with the Swiss ISO20022 standard if no sequence of nodes defined below
            occurring along the same path (in the same order) can be found.
            Examples:
                - ('PmtTpInf',) means that the tree cannot contain the tag <PmtTpInf>
                - ('ReqdExctnDt', 'Dt') means that the tag <ReqdExctnDt> cannot contain a tag <Dt>
        """
        forbidden_tag_sequences = (
            ('PmtTpInf',),
            ('BICFI',),
            ('ReqdExctnDt', 'Dt'),
            ('CdtrAgt', 'Othr'),
            ('DbtrAgt', 'Othr'),
        )

        self.bank_journal['sepa_pain_version'] = 'pain.001.001.09'

        payment = self.env['account.payment'].create({
            'journal_id': self.company_data['default_journal_bank'].id,
            'payment_method_line_id': self.payment_method_line.id,
            'payment_type': 'outbound',
            'date': '2024-03-04',
            'amount': 500,
            'partner_id': self.swiss_partner.id,
            'partner_bank_id': self.swiss_partner_bank.id,
            'partner_type': 'supplier',
            'memo': 'here',
        })
        payment.action_post()

        batch = self.env['account.batch.payment'].create({
            'journal_id': self.bank_journal.id,
            'payment_ids': [Command.link(payment.id)],
            'payment_method_id': self.payment_method.id,
            'batch_type': 'outbound',
        })

        wizard_action = batch.validate_batch()
        self.assertIsNone(wizard_action)
        batch.sudo().with_context(sepa_payroll_sala=True)._send_after_validation()
        tree = self.get_sct_doc_from_batch(batch)

        found_sequences = ""
        for seq in forbidden_tag_sequences:
            if tree.xpath("".join([f"//*[local-name()='{tag}']" for tag in seq])):
                found_sequences += "\n\t- " + " > ".join(seq)
        self.assertFalse(found_sequences, f"Forbidden tag sequence(s) found in XML: {found_sequences}")
