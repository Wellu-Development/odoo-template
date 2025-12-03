from odoo import models, fields

class NenaCustomerCategory(models.Model):
    _name = 'nena.customer.category'
    _description = 'Customer Category'

    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_unique",
            "UNIQUE(name)",
            "La descripción debe ser única.",
        )
    ]

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Description', required=True)
    nomedicine = fields.Boolean(string='No Medicine')
    is_website_available = fields.Boolean(string='Web Site', default=False)
    active = fields.Boolean(string='Active', default=True)
    product_category_id = fields.Many2many('product.category', string='Product Category')