from odoo import models, fields, api

class District(models.Model):
    _name = "district"
    _sql_constraints = [
        (
            "nena_commercial_structure_codregion_unique",
            "UNIQUE(code)",
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

    ref = fields.Char(required=False)

    active = fields.Boolean(default=True)

    region_id = fields.Many2one("region")