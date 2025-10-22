from odoo import models, fields

class NenaCauseStatus(models.Model):
    _name = "nena.cause.status"
    _description = "General Status Cause"

    description = fields.Text(required=True)
    postulation_type_id = fields.Many2one('postulation.type')
    nena_gen_status_id = fields.Many2one('nena.gen.status')
