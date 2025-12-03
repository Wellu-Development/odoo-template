from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class NenaDocumentApproverLine(models.Model):
    _name = "nena.document.approver.line"
    _description = 'Document Approver Line'
    _rec_name = 'department_id'

    activity_type_id = fields.Many2one('mail.activity.type', string="Activity Type")
    department_id = fields.Many2one('hr.department', string="Department")
    nena_attachment_line_id = fields.Many2one('nena.attachment.line', string="Permits and Documents")
    employee_ids = fields.Many2many('hr.employee', string="Employee")
    required = fields.Boolean(string="Required")
    sequence = fields.Integer(string="Sequence")