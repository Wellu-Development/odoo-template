from odoo import models, fields
from odoo.exceptions import ValidationError

class NenaCustomerClasification(models.Model):
    _name = "nena.customer.clasification"
    _description = "Customer Clasification"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code,description)",
            "El código de la clasificación del cliente debe de ser unico",
        )
    ]

    code = fields.Integer(string="Codigo", required=True)
    description = fields.Char(string="Descripcion", required=True)
    amount_from = fields.Float(string="Monto desde", required=True)
    amount_until = fields.Float(string="Monto hasta", required=True)
    gen_management_id = fields.Many2one('nena.gen.management', string="Tipo", required=True)
    ref = fields.Integer(string="Referencia", required=True, help="Código de clasificación asociado a nena")            
    active = fields.Boolean(string="Activo", default=True)    