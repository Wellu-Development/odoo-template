from odoo import models, fields, api

class NenaChainCreditConditions(models.Model):
    _name = 'nena.chain.credit.conditions'
    _description = 'Condiciones de Crédito de la Cadena Comercial de los Clientes Nena'
    _inherit = 'nena.credit.conditions'

    _sql_constraints = [
        (
            'chain_id_unique',
            'UNIQUE(chain_id)',
            'Esta Condición Crediticia ya está asignada a otro expediente.'
        )
    ]

    chain_id = fields.Many2one('nena.chain', compute='compute_stage', inverse='stage_inverse', string='Cadenas') 
    chain_credit_ids = fields.One2many('nena.chain', 'chain_credit_id') 

    @api.depends('chain_credit_ids') 
    def compute_stage(self): 
        if len(self.chain_credit_ids) > 0: 
            self.chain_id = self.chain_credit_ids[0] 

    def stage_inverse(self): 
        if len(self.chain_credit_ids) > 0: 
            stage = self.env['nena.chain'].browse(self.chain_credit_ids[0].id) 
            asset.chain_credit_id = False             
        self.chain_id.chain_credit_id = self