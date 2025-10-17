from odoo import models, fields

class NenaGroup(models.Model):
    _name = 'nena.group'
    _description = 'Grupos de Clientes de Nena'

    _sql_constraints = [
        ('code_group_uniq', 'unique(code_group)', 'El código del grupo debe ser único.'),
    ]

    code_group = fields.Char(string='Código de Grupo', required=True)
    name = fields.Char(string='Nombre de Grupo', required=True)
    description = fields.Text(string='Descripción')
    #chain_ids = fields.Many2many('nena.chain', string='Cadenas de Valor') # Falta el modelo de cadenas
    #Falta agregar relacion con cadenas de clientes