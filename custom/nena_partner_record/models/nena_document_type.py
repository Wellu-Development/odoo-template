from odoo import models, fields

class NenaDocumentType(models.Model):
    _name = "nena.document.type"

    _sql_constraints = [
        (
            "name_unique",
            "UNIQUE(name)",
            "El nombre del documento y/o permiso debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    postulation_type_id = fields.Many2one('nena.postulation.type')
    customer_type_id = fields.Many2one('nena.customer.category')
    supplier_type_id = fields.Many2one('nena.supplier.type')
    product_type_id = fields.Many2one('product.category')
    regulatory_entity_id = fields.Many2one('nena.regulatory.entity')
    approver_ids = fields.One2many('nena.document.approver','document_type_id', string="Approvers")
    is_validity = fields.Boolean(string="Validity?")
    active = fields.Boolean(default=True)
    is_due_date = fields.Boolean()
    is_multiple_file = fields.Boolean(string="Multiple files?")