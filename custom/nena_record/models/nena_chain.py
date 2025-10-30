from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NenaChain(models.Model):
    _name = "nena.chain"
    _description = 'Cadenas de Clientes de Nena'
    _rec_name = "name"

    _sql_constraints = [
    (
        'name_unique', 
        'unique(name)', 
        'El nombre de la cadena debe ser único.')
    ]

    name = fields.Char(string='Cadena', required=True)
    codchain = fields.Char(string='Código', required=True)
    commercialduct = fields.Float(string='Descuento Comercial')
    promptpaymentdiscount = fields.Float(string='Descuento Pronto Pago')
    
    status_id = fields.Many2one('nena.gen.status', string="Estatus", required=True)
    cause_status_id = fields.Many2one('nena.cause.status', string="Causa del Estatus", required=True)
    group_id = fields.Many2one('nena.group', string='Grupos de Cadenas')
    chain_credit_id = fields.Many2one('nena.chain.credit.conditions', string='Condición Crediticia')

    condition_ids = fields.Many2many(
        'nena.condition',
        'nena_chain_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )

    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_chain = self.chain_credit_id
        if not credit_chain:
            credit_chain = self.env['nena.chain.credit.conditions'].create({
                'code': self.codchain or 'CC-001',
                'name': self.name or 'Nueva Condición' 
            })
            self.chain_credit_id = credit_chain
            
        return {
            'name': "Condiciones Crediticias", 
            'type': 'ir.actions.act_window',
            'res_model': 'nena.chain.credit.conditions', 
            'view_mode': 'form',
            'res_id': credit_chain.id, 
            'target': 'new', 
            'context': {
                'default_chain_id': self.id
            }
        }