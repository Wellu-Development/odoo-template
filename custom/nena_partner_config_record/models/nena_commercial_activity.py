from odoo import models, fields

class NenaCommercialActivity(models.Model):
    _name = 'nena.commercial.activity'
    _description = 'Actividad Comercial'
    _rec_name = "name"

    _sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code)",
            "El código debe de ser unico",
        )
    ]

    code = fields.Char(string='Codigo', required=True)
    name = fields.Char(string='Actividad')