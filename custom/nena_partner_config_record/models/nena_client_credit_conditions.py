from odoo import models, fields, api

class NenaClientCreditConditions(models.Model):
    _name = 'nena.client.credit.conditions'
    _description = 'Condiciones de Crédito de los Clientes Nena'
    _inherit = 'nena.credit.conditions'

    # references
    #client_id = fields.Many2one('chain', string='Cliente Comercial')

    # constraints
    #_sql_constraints = [
        #('unique_client_id', 'unique(user_id)', 'Cada usuario solo puede tener una condición de crédito asociada.')
    #]
    