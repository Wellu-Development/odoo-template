from odoo import models, fields, api

class NenaClientCreditConditions(models.Model):
    _name = 'nena.client.credit.conditions'
    _description = 'Condiciones de Crédito de los Clientes Nena'
    _inherit = 'nena.credit.conditions'

    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Clientes') 
    client_credit_ids = fields.One2many('nena.record', 'client_credit_id') 

    @api.depends('client_credit_ids') 
    def compute_stage(self): 
        if len(self.client_credit_ids) > 0: 
            self.record_id = self.client_credit_ids[0] 