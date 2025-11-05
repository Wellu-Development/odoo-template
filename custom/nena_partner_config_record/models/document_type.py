from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DocumentType(models.Model):
    _name = "document.type"
    _sql_constraints = [
        (
            "nena_partner_config_record_document_type_name_unique",
            "UNIQUE(name)",
            "El nombre del documento y/o permiso debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    customer_type_id = fields.Many2one('customer.type')
    supplier_type_id = fields.Many2one('supplier.type')
    regulatory_entity_id = fields.Many2one('regulatory.entity')
    product_type_id = fields.Many2one('product.type')
    active = fields.Boolean(default=True)
    is_due_date = fields.Boolean()
    is_multiple_file = fields.Boolean()
