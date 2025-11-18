from odoo import models, fields

class DocumentType(models.Model):
    _name = 'nena.document.type'
    _description = 'Document Type'
    _rec_name = "name"

    name = fields.Char(string='Documento', required=True)
    definition = fields.Text(string='Definiciòn')
    active = fields.Boolean(string='Activo', default=True)