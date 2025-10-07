from odoo import models, fields


class NenaExample(models.Model):
    _name = "nena.example"
    _description = "Nena Example"

    example = fields.Char(string="Example Field")
