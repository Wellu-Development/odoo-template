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
        default_status_code = 'CAD-01'
        new_status_chain = self.env['nena.gen.status'].search([('code', '=', default_status_code)], limit=1)
        if new_status_chain:
            res['status_id'] = new_status_chain.id 

        default_cause_status_code = '034'
        new_cause_status = self.env['nena.cause.status'].search([('code', '=', default_cause_status_code)], limit=1)
        if new_cause_status:
            res['cause_status_id'] = new_cause_status.id

        return res

    # Botones de Accion
    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_record = self.chain_credit_id
        if not credit_record:
            credit_record = self.env['nena.chain.credit.conditions'].create({
                'code': self.codchain or 'CA-001',
                'name': self.name or 'Nueva Condición' 
            })
            self.chain_credit_id = credit_record
            
        return {
            'name': "Condiciones Crediticias", 
            'type': 'ir.actions.act_window',
            'res_model': 'nena.chain.credit.conditions', 
            'view_mode': 'form',
            'res_id': credit_record.id, 
            'target': 'new', 
            'context': {
                'default_record_id': self.id
            }
        }