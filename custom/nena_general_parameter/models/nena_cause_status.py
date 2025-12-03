from odoo import models, fields

class NenaCauseStatus(models.Model):
    _name = "nena.cause.status"
    _description = "Status Cause"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "name_status_unique",
            "UNIQUE(name, gen_status_id)",
            "La combinación de descripción y estatus debe ser única.",
        )
    ]

    code = fields.Char(string='Code', readonly=True)
    name = fields.Text(string="Description", required=True)
    gen_status_id = fields.Many2one('nena.gen.status', string="Status")