from odoo import models, fields

class NenaCustomerCondition(models.Model):
    _name = "nena.customer.condition"
    _description = "Customer Condition"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_category_unique",
            "UNIQUE(code, category)",
            "El Codigo debe ser único.",
        ),
        (
            "description_category_unique",
            "UNIQUE(description, category)",
            "La descripción debe ser única.",
        )
    ]

    code = fields.Char(string='Code', size=3, default='000')
    description = fields.Char(string="Description", required=True)

    category = fields.Selection(
        [("VTA", "Ventas"), 
         ("COB", "Cobranzas"), 
         ("REG", "Regencia"), 
         ("ALM", "Almacen"), 
         ("CAD", "Cadena")],
        string="Category"
    )