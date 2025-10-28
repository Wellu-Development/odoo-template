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

    # Relacion de UNO A UNO
    availibity_ids = fields.One2many('nena.availability', 'chain_ids')
    chain_ids = fields.Many2one('nena.availability', string='Cadena')

    condition_ids = fields.Many2many(
        'nena.condition',
        'chain_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )



