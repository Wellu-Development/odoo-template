from odoo import models, fields

class NenaGroup(models.Model):
    _name = 'nena.group'
    _description = 'Groups'
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'El código del grupo debe ser único.'),
    ]

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    chain_ids = fields.One2many('nena.chain', 'group_id', string='Chains')