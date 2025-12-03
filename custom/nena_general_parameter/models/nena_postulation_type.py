from odoo import models, fields

class NenaPostulationType(models.Model):
    _name = "nena.postulation.type"
    _description = 'Postulation Type'
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

    code = fields.Char()
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
