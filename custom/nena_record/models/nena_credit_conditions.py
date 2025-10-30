from odoo import models, fields, api

class NenaCrediConditions(models.Model):
    _name = 'nena.credit.conditions'
    _description = 'Condiciones de Crédito para Clientes'

    code = fields.Char(string='Codigo')
    name = fields.Char(string='Cliente/Cadena')
    balance = fields.Float(string='Saldo', readonly=True, default=0)
    credit_limit = fields.Float(string='Límite de Crédito', default=0, required=True)
    permit_overdraft = fields.Float(string='Monto Permiso', readonly=True, default=0)
    transit_amount = fields.Float(string='Monto en Tránsito', readonly=True, default=0)
    prepaid_amount = fields.Float(string='Monto Prepagado', readonly=True, default=0)
    availability_amount = fields.Float(string='Disponibilidad',  compute='compute_total_available')
    user_transit_sum = fields.Float(string='Suma Tránsito de Usuarios', compute='compute_transit_amount')
    notes = fields.Text(string='Notas Adicionales')

    @api.depends('credit_limit', 'balance', 'transit_amount', 'prepaid_amount', 'permit_overdraft')
    def compute_total_available(self):
        for record in self:
            credit_conditions_amount = (-1 * record.transit_amount) + record.prepaid_amount

            if record.permit_overdraft <= 0 :
                record.availability_amount = (record.credit_limit - record.balance) + credit_conditions_amount
            else:
                record.availability_amount = record.permit_overdraft + credit_conditions_amount