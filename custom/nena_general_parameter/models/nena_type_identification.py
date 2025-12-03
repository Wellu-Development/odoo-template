from odoo import models, fields

class NenaTypeIdentification(models.Model):
    _name = 'nena.type.identification'
    _description = 'Type Identification'
    _rec_name = "name"

    name = fields.Char(string='Document', required=True)
    definition = fields.Text(string='Definition')
    active = fields.Boolean(string='Active', default=True)