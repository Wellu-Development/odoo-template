from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PostulationType(models.Model):
    _name = "postulation.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_postulation_type_name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de postulacion debe de ser unico",
        )
    ]

    name = fields.Char(required=True)

    code = fields.Char()

    active = fields.Boolean(default=True)

    @api.constrains("code")
    def _check_unique_code(self):
        for postulation in self:
            if not postulation.code:
                continue

            is_exists_postulation = postulation.search(
                [("code", "=", postulation.code)]
            )

            if len(is_exists_postulation) > 1:
                raise ValidationError("El codigo de la postulacion debe de ser unico")
