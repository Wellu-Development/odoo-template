from odoo import models, fields

class NenaRecordConfig(models.Model):
    _name = "nena.record.config"
    _description = 'Configuracion Expediente'

    _sql_constraints = [
        (
            "nena_partner_config_record_partner_config_record_name_unique",
            "UNIQUE(name)",
            "El nombre de esta configuración debe de ser único",
        )
    ]

    name = fields.Char(required=True)
    customer_type_ids = fields.Many2many('nena.customer.category')
    supplier_type_ids = fields.Many2many('nena.supplier.type')
    postulation_type_id = fields.Many2one('nena.postulation.type')
    product_type_ids = fields.Many2many('product.category')
    document_type_ids = fields.Many2many('nena.document.type')
    active = fields.Boolean(default=True)
