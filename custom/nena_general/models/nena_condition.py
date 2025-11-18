from odoo import models, fields, api

class NenaCondition(models.Model):
    _name = "nena.condition"
    _description = "Condition"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_management_unique",
            "UNIQUE(description, gen_management_id)",
            "La combinación de descripción y tipo de gestion debe ser única.",
        )
    ]

    code = fields.Char(string='Código', copy=False, default='000')
    description = fields.Char(string="Descripcion", required=True)
    ref = fields.Integer(string="Referencia")
    gen_management_id = fields.Many2one('nena.gen.management', string="Tipo de Gestión", required=True)