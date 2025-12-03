from odoo import models, fields, api

class NenaCreditConditionsCustomer(models.Model):
    _name = 'nena.credit.conditions.customer'
    _description = 'Customer Availability'
    _inherit = 'nena.credit.conditions'

    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Customer') 
    customer_credit_ids = fields.One2many('nena.record', 'customer_credit_id') 

    @api.depends('customer_credit_ids') 
    def compute_stage(self): 
        if len(self.customer_credit_ids) > 0: 
            self.record_id = self.customer_credit_ids[0] 