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
    ctacontablesap = fields.Char(string="Cta. Contable")
    codsap = fields.Char(string="Codigo SAP")
    ref = fields.Char(string="Referencia", required=False)
    active = fields.Boolean(string="Activo", default=True)

    district_id = fields.Many2one("nena.district")