from odoo import models, fields, api

class NenaChainCreditConditions(models.Model):
    _name = 'nena.chain.credit.conditions'
    _description = 'Condiciones de Crédito de la Cadena Comercial de los Clientes Nena'
    _inherit = 'nena.credit.conditions'

    # references
    #chain_id = fields.Many2one('chain', string='Cadena Comercial')

    # constraints
    #_sql_constraints = [
    #    ('unique_chain_id', 'unique(chain_id)', 'Cada cadena solo puede tener una condición de crédito asociada.')
        #('unique_user_id', 'unique(user_id)', 'Cada usuario solo puede tener una condición de crédito asociada.')
    #]
    