from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductType(models.Model):
    _name = "product.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_product_type_name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de producto debe de ser único",
        ),
        (
            "nena_partner_config_record_product_type_code_unique",
            "UNIQUE(code)",
            "El código del tipo de producto debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char()
    is_website_available = fields.Boolean(default=False)
    customer_type_id = fields.Many2one('customer.type')
    supplier_type_id = fields.Many2one('supplier.type')
    active = fields.Boolean(default=True)
