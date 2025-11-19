from odoo import models, fields

class NenaCauseStatus(models.Model):
    _name = "nena.cause.status"
    _description = "General Status Cause"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_gen_status_unique",
            "UNIQUE(description, gen_status_id)",
            "La combinación de descripción y estatus debe ser única.",
        )
    ]

    code = fields.Char(string='Código', readonly=True)
    description = fields.Text(required=True)
    gen_status_id = fields.Many2one('nena.gen.status', string="Estatus")