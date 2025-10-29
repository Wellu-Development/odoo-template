from odoo import models, fields

class PaymentType(models.Model):
    _name = "payment.type"
    _description = "Customer payment type"
    _order = "description asc"
    _sql_constraints = [
        (
            "nena_partner_payment_method_payment_type_description_unique",
            "UNIQUE(description)",
            "La descripción del método de pago debe ser único",
        )
    ]

    
    description = fields.Char(string=f'Descripción',required=True)
    active = fields.Boolean(string='Activo', default=True) 
    ref = fields.Char(string=f'Referencia',required=True)