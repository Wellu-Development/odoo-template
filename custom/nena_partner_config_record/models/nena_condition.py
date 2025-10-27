from odoo import models, fields

class NenaCondition(models.Model):
    _name = "nena.condition"
    _description = "Condition"
    _rec_name = "description"
    _sql_constraints = [
        (
            "description_category_unique",
            "UNIQUE(description, category_id)",
            "La combinación de descripción y categoría debe ser única.",
        )
    ]

    description = fields.Char(string="Descripcion", required=True)
    ref = fields.Integer(string="Referencia", required=True)

    category_id = fields.Many2one('nena.condition.category', string="Categoria")