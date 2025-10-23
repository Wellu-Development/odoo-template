from odoo import models, fields, api

class Zone(models.Model):
    _name = "zone"
    _sql_constraints = [
        (
            "nena_commercial_structure_codzone_unique",
            "UNIQUE(code)",
            "El codigo de la zona debe ser unico",
        ),
        (
            "nena_commercial_structure_zone_unique",
            "UNIQUE(name)",
            "El nombre de la zona debe ser unico",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    ref = fields.Char(required=False)
    active = fields.Boolean(default=True)

    district_id = fields.Many2one("district")