from odoo import models, fields

class NenaCondition(models.Model):
    _name = "nena.condition"
    _description = "Condition"

    description = fields.Char(string="Description", required=True)
    category = fields.Selection(selection=[
        ("cadena","Cadena"),
        ("ventas","Ventas"),
        ("regencia","Regencia"),
        ("cobranza","Cobranza"),
        ("despacho","Despacho"),
        ], string="Category", required=True)
    ref = fields.Integer(string="Reference", required=True)
