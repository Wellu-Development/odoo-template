from odoo import models, fields

class NenaConfigCollectionManagement(models.Model):
    _name = "nena.config.collection.management"
    _description = 'Collection Management'

    name = fields.Char(string='Name', required=True)
    max_credit_limit = fields.Float(string='Maximum Credit Limit', default=0, required=True)
    max_permit_overdraft = fields.Float(string='Maximum Permit Amount', default=0, required=True)
    allow_permit_overdraft = fields.Boolean(string='Allow Grant Permission', default=False)
    notes = fields.Text(string='Additional Notes')
    employee_ids = fields.One2many("hr.employee", "config_collection_management_id", string="Employee")