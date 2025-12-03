from odoo import models, fields

class NenaCustomerClasification(models.Model):
    _name = "nena.customer.clasification"
    _description = "Customer Clasification"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code, category)",
            "El Codigo debe ser único.",
        ),
        (
            "description_category_unique",
            "UNIQUE(description, category)",
            "La descripción debe ser única.",
        )
    ]

    code = fields.Integer(string="Code", required=True)
    description = fields.Char(string="Description", required=True)
    amount_from = fields.Float(string="Amount from", required=True)
    amount_until = fields.Float(string="Amount to", required=True)
    active = fields.Boolean(string="Active", default=True)    

    category = fields.Selection(
        [("CLI", "Cliente"), 
         ("CAD", "Cadena")],
        string="Category"
    )