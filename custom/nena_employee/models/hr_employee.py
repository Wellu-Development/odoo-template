from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    config_collection_management_id = fields.Many2one("nena.config.collection.management", string="Availability")
    zone_ids = fields.Many2many("nena.zone")
    job_id_is_analyst = fields.Boolean(related="job_id.is_collections_analyst")

    @api.onchange("department_id")
    def _onchange_department_id(self):
        if self.department_id:
            self.job_id = False