from odoo import models, fields

class NenaPersonType(models.Model):
    _name = 'nena.person.type'
    _description = 'Person Type'
    _rec_name = "name"
    
    name = fields.Text(string='Description')