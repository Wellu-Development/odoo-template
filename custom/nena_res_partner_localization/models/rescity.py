from odoo import models, fields

class ResCity(models.Model):
    _inherit = "res.city"

    municipality_id = fields.Many2one(
        "nena.res.country.municipality", string="Municipality"
    )

    code = fields.Char(string="Code")