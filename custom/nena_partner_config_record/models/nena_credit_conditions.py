from odoo import models, fields, api

class nena_credit_conditions(models.Model):
    _name = 'nena.credit.conditions'
    _description = 'Condiciones de Crédito para Clientes'


    # fields
    name = fields.Char(string='Nombre de la Condición de Crédito')
    balance = fields.Float(string='Límite de Saldo', readonly=True)
    credit_limit = fields.Float(string='Límite de Crédito', required=True)
    permit_overdraft = fields.Float(string='Monto Permiso',default=0)
    availability_amount = fields.Float(string='Disponibilidad',  compute='compute_total_available')
    transit_amount = fields.Float(string='Monto en Tránsito', default=0)
    prepaid_amount = fields.Float(string='Monto Prepagado', default=0)
    user_transit_sum = fields.Float(string='Suma de Tránsito de Usuarios', compute='compute_transit_amount')
    notes = fields.Text(string='Notas Adicionales')

    # references
    #chain_id = fields.Many2one('chain', string='Cadena Comercial')

    # constraints
    #_sql_constraints = [
    #    ('unique_chain_id', 'unique(chain_id)', 'Cada cadena solo puede tener una condición de crédito asociada.')
        #('unique_user_id', 'unique(user_id)', 'Cada usuario solo puede tener una condición de crédito asociada.')
    #]
    
    # computed fields
    @api.depends('credit_limit', 'balance', 'transit_amount', 'prepaid_amount', 'permit_overdraft')
    def compute_total_available(self):
        for record in self:
            credit_conditions_amount = (-1 * record.transit_amount) + record.prepaid_amount

            if record.permit_overdraft <= 0 :
                record.availability_amount = (record.credit_limit - record.balance) + credit_conditions_amount
            else:
                record.availability_amount = record.permit_overdraft + credit_conditions_amount

