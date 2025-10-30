from odoo import models, fields, api

class NenaClientCreditConditions(models.Model):
    _name = 'nena.client.credit.conditions'
    _description = 'Condiciones de Crédito de los Clientes Nena'
    _inherit = 'nena.credit.conditions'

    _sql_constraints = [
        (
            'record_id_unique',
            'UNIQUE(record_id)',
            'Esta Condición Crediticia ya está asignada a otro expediente.'
        )
    ]

    record_id = fields.Many2one('nena.record', compute='compute_stage', inverse='stage_inverse', string='Clientes') 
    client_credit_ids = fields.One2many('nena.record', 'client_credit_id') 

    @api.depends('client_credit_ids') 
    def compute_stage(self): 
        if len(self.client_credit_ids) > 0: 
            self.record_id = self.client_credit_ids[0] 

    def stage_inverse(self): 
        if len(self.client_credit_ids) > 0: 
            stage = self.env['nena.record'].browse(self.client_credit_ids[0].id) 
            asset.client_credit_id = False             
        self.record_id.client_credit_id = self