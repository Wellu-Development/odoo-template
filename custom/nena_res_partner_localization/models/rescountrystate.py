from odoo import models, fields

class ResCountryState(models.Model):
    _inherit = "res.country.state"

    municipality_ids = fields.One2many(
        "nena.res.country.municipality", "state_id", string="Municipalities"
    )
