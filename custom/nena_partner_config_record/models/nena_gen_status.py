from odoo import models, fields

class NenaGenStatus (models.Model):

    _name = "nena.gen.status"
    _description = "General Status"

    description = fields.Text()

    postulation_type_id = fields.Many2one('postulation.type')
    