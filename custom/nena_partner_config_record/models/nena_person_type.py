from odoo import models, fields

class NenaPersonType(models.Model):
    _name = 'nena.person.type'
    _description = 'Tipo de Persona'
    _rec_name = "name"
    
    name = fields.Text(string='Descripcion')