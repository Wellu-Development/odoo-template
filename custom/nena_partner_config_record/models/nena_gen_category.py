from odoo import models, fields

class NenaGenCategory(models.Model):
    _name = "nena.gen.category"
    _description = "General Category"
    _rec_name = "code"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "category_unique",
            "UNIQUE(category)",
            "La Categoria debe ser única.",
        )
    ]

    code = fields.Char(string="Tipo", size=3, required=True)
    category = fields.Char(string="Descripcion", required=True)
    active = fields.Boolean(string="Actvo")
    entity = fields.Boolean(string="Entidad")
    operational = fields.Boolean(string="Operativo")