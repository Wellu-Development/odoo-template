from odoo import models, fields

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'
    
    ref = fields.Char(string='Codigo', size=4) 