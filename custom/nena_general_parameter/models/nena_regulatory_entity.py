from odoo import models, fields

class NenaRegulatoryEntity(models.Model):
    _name = "nena.regulatory.entity"

    _sql_constraints = [
        (
            "name_unique",
            "UNIQUE(name)",
            "El nombre del del ente regulatorio debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    description = fields.Char(string="Description")
    active = fields.Boolean(default=True)