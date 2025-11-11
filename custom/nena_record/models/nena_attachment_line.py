from odoo import models, fields, api

class NenaAttachmentLine(models.Model):
    _name = "nena.attachment.line"
    _description = 'Documentos'
    _rec_name = "document_id"
    
    # _sql_constraints = [
    #     (
    #         "codzone_unique",
    #         "UNIQUE(code)",
    #         "El codigo de la zona debe ser unico",
    #     )
    # ]

    document_id = fields.Many2one("document.type", string="Documento")
    nena_record_id = fields.Many2one('nena.record', string="Expediente")
    regulatory_entity_id = fields.Many2one('regulatory.entity', related="document_id.regulatory_entity_id")
    postulation_type_id = fields.Many2one('postulation.type', related="document_id.postulation_type_id")
    approver_ids = fields.One2many('document.approver','document_type_id', string="Aprobadores", related="document_id.approver_ids")
    is_validity = fields.Boolean(string="Vigencia?", related="document_id.is_validity")
    is_multiple_file = fields.Boolean(string="Archivos multiples?", related="document_id.is_multiple_file")
    start_date = fields.Date()
    end_date = fields.Date(string="Fecha de vencimiento")
    approver_line_ids = fields.One2many('document.approver.line','nena_attachment_line_id', string="Aprobadores")
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