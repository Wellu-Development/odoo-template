from odoo import models, fields, api

class NenaRegion(models.Model):
    _name = "nena.region"
    _description = 'Region'
    _rec_name = "name"
    _sql_constraints = [
        (
            "codregion_unique",
            "UNIQUE(code)",
            "El codigo de la region debe ser unico",
        ),
        (
            "region_unique",
            "UNIQUE(name)",
            "El nombre de la region debe ser unico",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    codgerente = fields.Char()
    ref = fields.Char(required=False)
    is_website_available = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    district_ids = fields.One2many("nena.district", "region_id")