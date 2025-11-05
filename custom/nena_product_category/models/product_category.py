from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    reference = fields.Char(string="Referencia")
    color = fields.Char(string="Color")
    controlled = fields.Boolean(string="Es controlado?")