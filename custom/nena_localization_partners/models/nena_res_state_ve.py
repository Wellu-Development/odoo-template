from odoo import fields, models

class NenaResStateVe(models.Model):
    _name = "nena.res.state.ve"
    _rec_name = "name"
    _description = "Localized state for partner address"

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name,country_id)",
            "A state with this name already exists for the selected country.",
        )
    ]

    country_id = fields.Many2one("res.country", string="Country", required=True)
    name = fields.Char(string="State", required=True)
    code = fields.Char(string="Code", required=True)
    ref = fields.Char(string="Reference")

    municipality_ids = fields.One2many(
        "nena.res.state.municipality.ve",
        "state_id",
        string="Municipalities",
    )