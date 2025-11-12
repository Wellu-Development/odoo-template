from odoo import models, fields

class NenaCustomerCategory(models.Model):
    _name = 'nena.customer.category'
    _description = 'Categoría de Cliente'
    _rec_name = "name"

    code = fields.Char(string='Codigo', required=True)
    name = fields.Text(string='Nombre')
    nomedicine = fields.Boolean(string='NoMedicina')
    websiteavaible = fields.Boolean(string='Web Site')
    active = fields.Boolean(string='Activo')

    product_category_id = fields.Many2one('product.category', string='Categorías de Producto')