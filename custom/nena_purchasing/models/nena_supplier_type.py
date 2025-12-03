from odoo import models, fields

class NenaSupplierType(models.Model):
    _name = "nena.supplier.type"

    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de proveedor debe de ser único",
        )
    ]

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Description', required=True)
    is_website_available = fields.Boolean(string='Web Site', default=False)
    active = fields.Boolean(string='Active', default=True)
    product_category_id = fields.Many2many('product.category', string='Product Category')