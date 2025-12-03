from odoo import models, fields

class NenaAttachmentLine(models.Model):
    _name = "nena.attachment.line"
    _description = 'Documents'
    _rec_name = "document_id"
    
    document_id = fields.Many2one("nena.document.type", string="Document")
    nena_record_id = fields.Many2one('nena.record', string="Record")
    regulatory_entity_id = fields.Many2one('nena.regulatory.entity', related="document_id.regulatory_entity_id")
    postulation_type_id = fields.Many2one('nena.postulation.type', related="document_id.postulation_type_id")
    approver_ids = fields.One2many('nena.document.approver','document_type_id', string="Approvers", related="document_id.approver_ids")
    is_validity = fields.Boolean(string="Validity?", related="document_id.is_validity")
    is_multiple_file = fields.Boolean(string="Multiple files?", related="document_id.is_multiple_file")
    start_date = fields.Date()
    end_date = fields.Date(string="Expiration Date")
    approver_line_ids = fields.One2many('nena.document.approver.line','nena_attachment_line_id', string="Approvers")
    
    state = fields.Selection([
                ('draft', 'Solicitar documento'),
                ('waiting', 'Esperando documento'),
                ('to_verify', 'Por verificar'),
                ('verified', 'Verificado'),
                ('rejected', 'Rechazado'),
                ('valid', 'Vigente'),
                ('expired', 'Vencido')
            ], string='Tipo', default='draft')
    
    def action_verified(self):
        return True
    
    def action_refuse(self):
        return True