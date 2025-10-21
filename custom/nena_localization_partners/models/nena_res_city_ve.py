from odoo import fields, models

class NenaResMunicipalityCity(models.Model):
    _name = "nena.res.state.municipality.city.ve"
    _rec_name = "name"
    _description = "Localized city for partner address"

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name, municipality_id)",
            "A city with this name already exists for the selected municipality.",
        )
    ]

    municipality_id = fields.Many2one("nena.res.state.municipality.ve", string="Municipality", required=True)
    name = fields.Char(string="City", required=True)
    code = fields.Char(string="Code", required=True)
    ref = fields.Char(string="Reference")