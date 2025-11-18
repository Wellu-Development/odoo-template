from odoo import models, fields
from odoo.exceptions import ValidationError

class ProductSubType(models.Model):
    _name = "nena.product.subtype"
    _description = "Product Subtype"
    _inherit = ['mail.thread','mail.activity.mixin']

    _sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code,name,product_category_id)",
            "El código del subtipo de producto debe de ser único",
        )
    ]

    code = fields.Char(string="Código", required=True,tracking=True)
    name = fields.Char(string="Nombre", required=True,tracking=True)
    status = fields.Boolean(string="Estatus", default=True,tracking=True)
    product_category_id = fields.Many2one('product.category', string="Código tipo producto",tracking=True)
    ref = fields.Char(string="Referencia", required=True, help="Código de subtipo asociado a nena",tracking=True)  