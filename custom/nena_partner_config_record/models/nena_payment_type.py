from odoo import models, fields

class PaymentType(models.Model):
    _name = "nena.payment.type"
    _description = "Customer payment type"
    _rec_name = "description"
    _order = "description asc"

    _sql_constraints = [
        (
            "description_unique",
            "UNIQUE(description)",
            "La descripción del método de pago debe ser único",
        )
    ]

    description = fields.Char(string=f'Descripción',required=True)
    active = fields.Boolean(string='Activo', default=True) 