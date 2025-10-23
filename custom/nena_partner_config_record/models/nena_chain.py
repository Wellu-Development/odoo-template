from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NenaChain(models.Model):
    _name = "nena.chain"
    _sql_constraints = [
    (
        'unique_chain_name', 
        'unique(name)', 
        'El nombre de la cadena debe ser único.')
    ]

    name = fields.Char(string='Cadena', required=True)
    codchain = fields.Char(string='Código Cadena')
    
    status = fields.Char(string='Estatus')
    causestatus = fields.Char(string='Causa del Estatus')
    
    commercialduct = fields.Float(string='Descuento Comercial')
    promptpaymentdiscount = fields.Float(string='Descuento Pronto Pago')

    availibity_ids = fields.One2many('nena.availability', 'chain_ids', string='Disponibilidad Cadena')
    chain_ids = fields.Many2one('nena.availability', string='Cadena')
    group_id = fields.Many2one('nena.group', string='Grupos de Cadenas')
    # currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)



