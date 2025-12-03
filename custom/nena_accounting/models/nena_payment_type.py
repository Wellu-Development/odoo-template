from odoo import models, fields

class PaymentType(models.Model):
    _name = "nena.payment.type"
    _description = "Payment Type"
    _rec_name = "description"
    _order = "description asc"

    _sql_constraints = [
        (
            "description_unique",
            "UNIQUE(description)",
            "La descripción del método de pago debe ser único",
        )
    ]

    description = fields.Char(string=f'Description',required=True)
    active = fields.Boolean(string='Active', default=True) 