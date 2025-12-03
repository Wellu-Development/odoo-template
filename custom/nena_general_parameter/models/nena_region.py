from odoo import models, fields

class NenaRegion(models.Model):
    _name = "nena.region"
    _description = 'Region'
    
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

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    codgerente = fields.Char(string="Manager Code")
    active = fields.Boolean(string="Active", default=True)
    district_ids = fields.One2many("nena.district", "region_id", string="Districts")