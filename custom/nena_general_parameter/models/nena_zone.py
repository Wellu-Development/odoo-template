from odoo import models, fields

class NenaZone(models.Model):
    _name = "nena.zone"
    _description = 'Zone'
    _rec_name = "code"
    
    _sql_constraints = [
        (
            "codzone_unique",
            "UNIQUE(code)",
            "El codigo de la zona debe ser unico",
        )
    ]

    code = fields.Char(string="Code", required=True)
    description = fields.Char(string="Description", required=True)
    active = fields.Boolean(string="Active", default=True)
    district_id = fields.Many2one("nena.district", string="Districts")