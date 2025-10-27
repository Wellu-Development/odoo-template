from odoo import models, fields, api

class NenaDistrict(models.Model):
    _name = "nena.district"
    _description = 'Distrito'
    _rec_name = "name"
    _sql_constraints = [
        (
            "coddistrict_unique",
            "UNIQUE(code)",
            "El codigo del distrito debe ser unico",
        ),
        (
            "district_unique",
            "UNIQUE(name)",
            "El nombre del distrito debe ser unico",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    ref = fields.Char(required=False)
    active = fields.Boolean(default=True)
    
    region_id = fields.Many2one("nena.region")
    zones_ids = fields.One2many("nena.zone", "district_id")