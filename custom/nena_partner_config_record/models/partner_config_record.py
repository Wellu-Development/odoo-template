from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PartnerConfigRecord(models.Model):
    _name = "partner.config.record"
    _sql_constraints = [
        (
            "nena_partner_config_record_partner_config_record_name_unique",
            "UNIQUE(name)",
            "El nombre de esta configuración debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    customer_type_ids = fields.Many2many('customer.type')
    supplier_type_ids = fields.Many2many('supplier.type')
    postulation_type_id = fields.Many2one('postulation.type')
    product_type_ids = fields.Many2many('product.type')
    document_type_ids = fields.Many2many('document.type')
    active = fields.Boolean(default=True)
