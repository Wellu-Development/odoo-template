from odoo import models, fields

class NenaCustomerCategory(models.Model):
    _name = 'nena.customer.category'
    _description = 'Categoría de Cliente'
    _rec_name = "name"

    code = fields.Char(string='Codigo', required=True)
    name = fields.Char(string='Descripcion')
    nomedicine = fields.Boolean(string='No Medicina')
    websiteavaible = fields.Boolean(string='Web Site')
    active = fields.Boolean(string='Activo')

    product_category_id = fields.Many2many('product.category', string='Categorías de Producto')