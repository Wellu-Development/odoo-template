from odoo import models, fields

class NenaHrJob(models.Model):
    _inherit = "hr.job"

    nena_hr_job_id = fields.Many2one("hr.department", string="Departamento")