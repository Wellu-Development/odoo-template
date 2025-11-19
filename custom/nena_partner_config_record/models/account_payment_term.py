from odoo import models, fields

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'
    
    postulation_type_id = fields.Many2one('postulation.type')
    ref = fields.Char(string='Codigo', size=4) 