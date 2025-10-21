from odoo import models, fields

class NenaCondition(models.Model):
    _name = "nena.condition"
    _description = "Condition"

    description = fields.Char(string="Description", required=True)
    ref = fields.Integer(string="Reference", required=True)

    category_id = fields.Many2one('nena.condition.category', string="Category")