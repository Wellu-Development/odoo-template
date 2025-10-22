from odoo import models, fields
from odoo.exceptions import ValidationError

class ClientClasificationClient(models.Model):
    _name = "client.clasification"
    _sql_constraints = [
        (
            "nena_client_clasification_client_clasification_code_unique",
            "UNIQUE(code,description)",
            "El código de la clasificación del cliente debe de ser unico",
        )
    ]

    code = fields.Integer(string="Codigo", required=True)
    description = fields.Char(string="Descripcion", required=True)
    amount_from = fields.Float(string="Monto desde", required=True)
    amount_until = fields.Float(string="Monto hasta", required=True)
    type = fields.Selection([
                ('cli', 'CLI'),
                ('cad', 'CAD')
            ], srting='Tipo', default='cli')
    ref = fields.Integer(string="Referencia", required=True, help="Código de clasificación asociado a nena")            
    active = fields.Boolean(string="Activo", default=True)    