from odoo import models, fields

class HrDepartment(models.Model):
    _inherit = "hr.department"

    hr_job_ids = fields.One2many("hr.job", "department_id", string="Occupation")