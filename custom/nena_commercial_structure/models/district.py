from odoo import models, fields, api

class District(models.Model):
    _name = "district"
    _sql_constraints = [
        (
            "nena_commercial_structure_coddistrict_unique",
            "UNIQUE(code)",
            "El codigo del distrito debe ser unico",
        ),
        (
            "nena_commercial_structure_district_unique",
            "UNIQUE(name)",
            "El nombre del distrito debe ser unico",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    ref = fields.Char(required=False)
    active = fields.Boolean(default=True)
    
    region_id = fields.Many2one("region")
    zones_ids = fields.One2many("zone", "district_id")