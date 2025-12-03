from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    composition_ids = fields.One2many(
        'nena.drug.composition',
        'product_id',
        string='Product Composition'
    )
