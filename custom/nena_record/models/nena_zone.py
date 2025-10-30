from odoo import models, fields, api

class NenaZone(models.Model):
    _name = "nena.zone"
    _description = 'Zona'
    _rec_name = "code"
    
    _sql_constraints = [
        (
            "codzone_unique",
            "UNIQUE(code)",
            "El codigo de la zona debe ser unico",
        )
    ]

    code = fields.Char(required=True)
    description = fields.Char(required=True)
    ctacontablesap = fields.Char()
    codsap = fields.Char()
    ref = fields.Char(required=False)
    active = fields.Boolean(default=True)

    district_id = fields.Many2one("nena.district")