from odoo import models, fields

class HrJob(models.Model):
    _inherit = "hr.job"

    is_approver_record = fields.Boolean(string="Approve File")
    is_collections_analyst = fields.Boolean(string="Collections Analyst")