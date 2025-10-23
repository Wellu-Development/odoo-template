from odoo import fields, models


class NenaResStateMunicipalityVe(models.Model):
    _name = "nena.res.state.municipality.ve"
    _rec_name = "name"
    _description = "Localized municipality for partner address"

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name, state_id)",
            "A municipality with this name already exists for the selected state.",
        )
    ]

    state_id = fields.Many2one("nena.res.state.ve", string="State", required=True)
    name = fields.Char(string="Municipality", required=True)
    code = fields.Char(string="Code")
    ref = fields.Char(string="Reference")