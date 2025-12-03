from odoo import models, fields

class NenaDistrict(models.Model):
    _name = "nena.district"
    _description = 'District'
    
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

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    region_id = fields.Many2one("nena.region", string="Regions")
    zones_ids = fields.One2many("nena.zone", "district_id", string="Zones")