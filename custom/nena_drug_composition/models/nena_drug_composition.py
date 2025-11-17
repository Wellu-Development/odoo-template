from odoo import models, fields

class DrugComposition(models.Model):
    _name = 'nena.drug.composition'
    _description = 'Drug Composition'

    reference = fields.Char(string='Reference', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    line_ids = fields.One2many('nena.drug.composition.line', 'composition_id', string='Principios Activos')
