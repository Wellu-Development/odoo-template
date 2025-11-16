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
    codchain = fields.Char(string='Código', size=4, required=True)
    commercialduct = fields.Float(string='Dcto. Comercial')
    promptpaymentdiscount = fields.Float(string='Dcto. Pronto Pago')
    status_id = fields.Many2one('nena.gen.status', string="Estatus")
    cause_status_id = fields.Many2one('nena.cause.status')
    group_id = fields.Many2one('nena.group', string='Grupos de Cadenas')
    client_ids = fields.One2many('nena.record', 'chain_id', string="Clientes")
    
    # Condición Crediticia
    chain_credit_id = fields.Many2one('nena.chain.credit.conditions')
    chain_credit_limit = fields.Float(string="Límite de Crédito", related="chain_credit_id.credit_limit", readonly=False)
    chain_credit_balance = fields.Float(string="Saldo", related="chain_credit_id.balance")
    chain_credit_transit = fields.Float(string='Monto Tránsito', related="chain_credit_id.transit_amount")
    chain_credit_prepaid = fields.Float(string="Monto Prepagado", related="chain_credit_id.prepaid_amount")
    chain_credit_availability = fields.Float(string='Disponibilidad', related="chain_credit_id.availability_amount")

    # Parametros de Cadena (Condiciones)
    condition_ids = fields.Many2many(
        'nena.condition',
        'nena_chain_condition_rel',
        'partner_id',
        'condition_id',
        string="Parametros"
    )

    # Valores por Defectos
    def default_get(self, fields_list):
        res = super(NenaChain, self).default_get(fields_list)
        
        # Valor por Defecto para Estatus
        default_status_chain_description = 'Activo'
        new_status_chain = self.env['nena.gen.status'].search([('description', '=', default_status_chain_description)], limit=1)
        if new_status_chain:
            res['status_id'] = new_status_chain.id 

        default_cause_status_description = 'Cliente al Di­a (Grupo)'
        new_cause_status = self.env['nena.cause.status'].search([('description', '=', default_cause_status_description)], limit=1)
        if new_cause_status:
            res['cause_status_id'] = new_cause_status.id

        return res