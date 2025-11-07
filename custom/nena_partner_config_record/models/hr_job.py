from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class HrJob(models.Model):
    _inherit = "hr.job"

    is_approver = fields.Boolean(string="Es aprobador?")