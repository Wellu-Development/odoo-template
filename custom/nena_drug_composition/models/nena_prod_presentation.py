from odoo import models, fields

class ProductPresentation(models.Model):
    _name = 'nena.prod.presentation'
    _description = 'Product Presentation'
    _rec_name = 'abbrev_presentation'

    reference = fields.Char(string='Reference')
    abbrev_presentation = fields.Char(string='Presentation Abreviada', size=10)
    description_presentation = fields.Char(string='Descripción de la Presentación', size=100)

    has_dosage = fields.Boolean(string='Tiene Dosificación', default=False)

    uom_presentation_id = fields.Many2one('uom.uom', string='Unidad de Medida')
    active = fields.Boolean(string='Active', default=True)