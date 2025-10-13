from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PostulationType(models.Model):
    _name = "postulation.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_postulation_type_name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de postulacion debe de ser único",
        ),
        (
            "nena_partner_config_record_postulation_type_code_unique",
            "UNIQUE(code)",
            "El código del tipo de postulacion debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    code = fields.Char()
    active = fields.Boolean(default=True)
