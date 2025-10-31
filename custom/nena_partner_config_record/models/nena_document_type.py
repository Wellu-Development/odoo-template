from odoo import models, fields

class DocumentType(models.Model):
    _name = 'nena.document.type'
    _description = 'Document Type'

    name = fields.Char(string='Document Type', required=True)
    definition = fields.Text(string='Definition')
    active = fields.Boolean(string='Active', default=True)