from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class NenaStatusManagement(models.Model):
    _name = "nena.gen.status"
    _description = "Status Management"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_model_field_unique",
            "UNIQUE(description, model_id, field_id)",
            "El Estatus debe ser único por Modelo.",
        )
    ]

    code = fields.Char(string='Code')
    name = fields.Char(string="Description", required=True)
    category = fields.Char(string="Category", required=True)
    model_id = fields.Many2one('ir.model', string="Associated Model")
    field_id = fields.Many2one('ir.model.fields', string="Associated Field", domain="[('model_id','=',model_id)]")
    cause_active = fields.Boolean(string="Manage by Causes", required=True)
    cause_status_ids = fields.One2many('nena.cause.status', 'gen_status_id', string="Causes")

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            if record.name:
                if len(record.name) > 50:
                    raise ValidationError("La descripción no puede tener más de 50 caracteres.")

                if re.search(r'\d', record.name):
                    raise ValidationError("La descripción no puede contener números.")