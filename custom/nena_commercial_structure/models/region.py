from odoo import models, fields, api

class Region(models.Model):
    _name = "region"
    _sql_constraints = [
        (
            "nena_commercial_structure_codregion_unique",
            "UNIQUE(code_region)",
            "El codigo de la region debe ser unico",
        ),
        (
            "nena_commercial_structure_region_unique",
            "UNIQUE(name)",
            "El nombre de la region debe ser unico",
        )
    ]
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    codgerente = fields.Char(required=True)
    ref = fields.Char(required=False)
    is_website_available = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    district_ids = fields.One2many("district", "region_id")