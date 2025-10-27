from odoo import models, fields

class PaymentType(models.Model):
    _name = "payment.type"
    _rec_name = "description"
    _sql_constraints = [
        (
            "nena_partner_payment_method_payment_type_description_unique",
            "UNIQUE(description)",
            "La descripción del metodo de pago debe ser unico",
        )
    ]

    
    description = fields.Char(string=f'Descripción',required=True)
    active = fields.Boolean(string='Activo', default=True)