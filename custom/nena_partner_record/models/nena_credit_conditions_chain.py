from odoo import models, fields, api

class NenaCreditConditionsChain(models.Model):
    _name = 'nena.credit.conditions.chain'
    _description = 'Availability Chain'
    _inherit = 'nena.credit.conditions'

    chain_id = fields.Many2one('nena.chain', compute='compute_stage', string='Chain') 
    chain_credit_ids = fields.One2many('nena.chain', 'chain_credit_id') 

    @api.depends('chain_credit_ids') 
    def compute_stage(self): 
        if len(self.chain_credit_ids) > 0: 
            self.chain_id = self.chain_credit_ids[0] 
