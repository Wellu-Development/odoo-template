from odoo import models, fields

class NenaDocumentApprover(models.Model):
    _name = "nena.document.approver"
    _description = 'Document Approver'
    _rec_name = 'department_id'

    activity_type_id = fields.Many2one('mail.activity.type', string="Type of activity")
    department_id = fields.Many2one('hr.department', string="Department")
    document_type_id = fields.Many2one('nena.document.type', string="Permits and Documents")
    employee_ids = fields.Many2many('hr.employee', string="Employees")
    required = fields.Boolean(string="Required")
    sequence = fields.Integer(string="Sequence")