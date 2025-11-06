from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class DocumentApprover(models.Model):
    _name = "document.approver"
    _description = 'Document Approver'
    _rec_name = 'department_id'

    activity_type_id = fields.Many2one('mail.activity.type', string="Tipo actividad")
    department_id = fields.Many2one('hr.department', string="Departamento")
    document_type_id = fields.Many2one('document.type', string="Permisos y documentos")
    employee_ids = fields.Many2many('hr.employee', string="Empleados")
    required = fields.Boolean(string="Requerido")
    sequence = fields.Integer(string="Secuencia")