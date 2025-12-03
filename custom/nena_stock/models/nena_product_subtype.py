from odoo import models, fields
from odoo.exceptions import ValidationError

class NenaProductSubType(models.Model):
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

    code = fields.Char(string="Code", required=True,tracking=True)
    name = fields.Char(string="Name", required=True,tracking=True)
    status = fields.Boolean(string="Status", default=True,tracking=True)
    product_category_id = fields.Many2one('product.category', string="Product Category",tracking=True)