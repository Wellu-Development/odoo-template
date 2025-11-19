from odoo import models, fields

class NenaHrDepartment(models.Model):
    _inherit = "hr.department"

    nena_gen_category_id = fields.Many2one("nena.gen.management", string="Area Operativa")
    job_ids = fields.One2many("hr.job", "nena_hr_job_id", string="Ocupaciones")


