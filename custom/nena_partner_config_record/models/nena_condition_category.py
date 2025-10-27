from odoo import models, fields

class NenaConditionCategory(models.Model):
    _name = "nena.condition.category"
    _description = "Condition Category"
    _rec_name = "category"
    _sql_constraints = [
        (
            "category_unique",
            "UNIQUE(category)",
            "La categoria debe ser única",
        )
    ]

    category = fields.Char(string="Categoria", required=True)