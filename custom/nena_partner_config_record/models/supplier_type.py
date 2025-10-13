from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SupplierType(models.Model):
    _name = "supplier.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_supplier_type_name_unique",
            "UNIQUE(name)",
            "El nombre del tipo de proveedor debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    is_website_available = fields.Boolean(default=False)
    active = fields.Boolean(default=True)
