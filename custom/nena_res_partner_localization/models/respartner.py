from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    municipality_id = fields.Many2one(
        "nena.res.country.municipality", string="Municipality"
    )

    @api.onchange("country_id")
    def _onchange_country_id(self):
        return {
            "domain": {
                "state_id": [("country_id", "=", self.country_id.id)],
                "municipality_id": [("country_id", "=", self.country_id.id)],
                "city_id": [("country_id", "=", self.country_id.id)],
            }
        }

    @api.onchange("state_id")
    def _onchange_state_id(self):
        return {
            "domain": {
                "municipality_id": [("state_id", "=", self.state_id.id)],
                "city_id": [("state_id", "=", self.state_id.id)],
            }
        }

    @api.onchange("municipality_id")
    def _onchange_municipality_id(self):
        return {
            "domain": {
                "city_id": [("municipality_id", "=", self.municipality_id.id)],
            }
        }
