from odoo import models, fields, api

class DrugActivePrinciple(models.Model):
    _name = 'nena.drug.active.principle'
    _description = 'Active Principle'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
