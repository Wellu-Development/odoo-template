from odoo import models, fields

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'
    
    postulation_type_id = fields.Many2one('nena.postulation.type')
    ref_nena = fields.Char(string='Code', size=4) 