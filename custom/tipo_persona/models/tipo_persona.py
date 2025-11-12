from odoo import models, fields

class TipoPersona(models.Model):
    _name = 'tipo.persona'
    _description = 'Tipo de Persona'
    _rec_name = "name"
    
    name = fields.Text(string='Valor')

