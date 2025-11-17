from odoo import models, fields
from odoo.exceptions import ValidationError

class ProductSubType(models.Model):
    _name = "nena.product.subtype"
    _description = "Product Subtype"
    _inherit = ['mail.thread','mail.activity.mixin']

    _sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code_subtype,name_subtype,product_category_id)",
            "El código del subtipo de producto debe de ser único",
        )
    ]

    code_subtype = fields.Char(string="Código", required=True)
    name_subtype = fields.Char(string="Nombre", required=True)
    status = fields.Boolean(string="Estatus", default=True)
    product_category_id = fields.Many2one('product.category', string="Código tipo producto")
    ref = fields.Char(string="Referencia", required=True, help="Código de subtipo asociado a nena")  