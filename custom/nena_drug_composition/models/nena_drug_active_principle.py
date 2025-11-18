from odoo import models, fields, api

class DrugActivePrinciple(models.Model):
    _name = 'nena.drug.active.principle'
    _description = 'Principio Activo'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
