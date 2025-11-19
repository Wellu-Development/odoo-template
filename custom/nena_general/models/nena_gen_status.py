from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class NenaStatusManagement(models.Model):
    _name = "nena.gen.status"
    _description = "Status Management"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_postulation_type_unique",
            "UNIQUE(description, gen_management_id)",
            "El Estatus debe ser único por Categoría.",
        )
    ]

    code = fields.Char(string='Código', readonly=True)
    description = fields.Char(required=True, string="Descripcion")
    gen_management_id = fields.Many2one('nena.gen.management', string="Tipo de Gestión", required=True)
    cause_active = fields.Boolean(required=True, string="Administrar por Causas")
    cause_status_ids = fields.One2many('nena.cause.status', 'gen_status_id', string="Causas")

    @api.constrains('description')
    def _check_description_constraints(self):
        for record in self:
            if record.description:
                if len(record.description) > 50:
                    raise ValidationError("La descripción no puede tener más de 50 caracteres.")

                if re.search(r'\d', record.description):
                    raise ValidationError("La descripción no puede contener números.")