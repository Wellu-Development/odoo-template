from odoo import models, fields

class NenaGenCategory(models.Model):
    _name = "nena.gen.category"
    _description = "General Category"
    _rec_name = "category"
    
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

    code = fields.Char(string="Codigo", size=3, required=True)
    category = fields.Char(string="Categoria", required=True)
    active = fields.Boolean(string="Actvo")
    use_condition = fields.Boolean(string="Condición")
    use_status = fields.Boolean(string="Estatus")