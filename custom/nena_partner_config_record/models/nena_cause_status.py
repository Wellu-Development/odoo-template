from odoo import models, fields

class NenaCauseStatus(models.Model):
    _name = "nena.cause.status"
    _description = "General Status Cause"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "description_gen_status_unique",
            "UNIQUE(description, nena_gen_status_id)",
            "La combinación de descripción y estatus debe ser única.",
        )
    ]

    description = fields.Text(required=True)
    postulation_type_id = fields.Many2one('postulation.type')
    nena_gen_status_id = fields.Many2one('nena.gen.status')
