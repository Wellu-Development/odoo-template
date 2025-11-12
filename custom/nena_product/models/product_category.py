from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"

    color = fields.Char(string="Color")
    controlled = fields.Boolean(string="Controlado")
    ref = fields.Char(string="Referencia")