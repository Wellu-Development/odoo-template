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
    commercialduct = fields.Float(string='Dcto. Comercial')
    promptpaymentdiscount = fields.Float(string='Dcto. Pronto Pago')
    status_id = fields.Many2one('nena.gen.status', string="Estatus", required=True)
    cause_status_id = fields.Many2one('nena.cause.status', string="Causa", required=True)
    group_id = fields.Many2one('nena.group', string='Grupos de Cadenas')
    client_ids = fields.One2many('nena.record', 'chain_id', string="Clientes")
    
    # Condición Crediticia
    chain_credit_id = fields.Many2one('nena.chain.credit.conditions')
    credit_limit = fields.Float(string="Límite de Crédito", related="chain_credit_id.credit_limit", readonly=False)
    balance = fields.Float(string="Saldo", related="chain_credit_id.balance")
    transit_amount = fields.Float(string='Monto en Tránsito', related="chain_credit_id.transit_amount")
    prepaid_amount = fields.Float(string="Monto Prepagado", related="chain_credit_id.prepaid_amount")
    availability_amount = fields.Float(string='Disponibilidad', related="chain_credit_id.availability_amount")

    # Parametros de Cadena (Condiciones)
    condition_ids = fields.Many2many(
        'nena.condition',
        'nena_chain_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )