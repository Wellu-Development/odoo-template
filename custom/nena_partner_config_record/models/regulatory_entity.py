from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RegulatoryEntity(models.Model):
    _name = "regulatory.entity"
    _sql_constraints = [
        (
            "nena_partner_config_record_supplier_type_name_unique",
            "UNIQUE(name)",
            "El nombre del del ente regulatorio debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
