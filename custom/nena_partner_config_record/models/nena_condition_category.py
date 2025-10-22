from odoo import models, fields

class NenaConditionCategory(models.Model):
    _name = "nena.condition.category"
    _description = "Condition Category"
    _rec_name = "category"

    category = fields.Char(string="Category", required=True)