from odoo import fields, models

class NenaResCountryMunicipality(models.Model):
    _name = "nena.res.country.municipality"
    _rec_name = "name"
    _description = "Localized municipality for partner address"

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name, state_id)",
            "A municipality with this name already exists for the selected state.",
        )
    ]

    name = fields.Char(string="Municipality", required=True)
    code = fields.Char(string="Code")
    country_id = fields.Many2one(comodel_name='res.country', string='Country', required=True)
    state_id = fields.Many2one(comodel_name='res.country.state', string='State', domain="[('country_id', '=', country_id)]")
    city_ids = fields.One2many("res.city", "municipality_id", string="Cities")
    