from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomerType(models.Model):
    _name = "customer.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_customer_type_name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de cliente debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    is_website_available = fields.Boolean(default=False)
    active = fields.Boolean(default=True)
