from odoo import models, fields,api

class NenaRegent(models.Model):
    _name = 'nena.regent'
    _description = 'Regent Data'

    document_type_id = fields.Many2one('nena.document.type', string='Tipo Documento', required=True)
    id_number = fields.Char(string='ID Numero', required=True)
    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Telefono')
    address = fields.Text(string='Direccion')
    matric_msds = fields.Char(string='MATRIC MSDS')
    colfar = fields.Char(string='COLFAR')
    inprefa_code = fields.Char(string='INPREFA')
    oper_min_start_date = fields.Date(string='Desde Acta Func.',required=True)
    oper_min_end_date = fields.Date(string='Hasta Acta Func.')
    sicm_code = fields.Char(string='Codigo S.I.C.M',required=True)
    sicm_status_id = fields.Many2one('nena.gen.status', string='Estatus S.I.C.M')
    sada_code = fields.Char(string='Codigo SADA',required=True)
    sada_status_id = fields.Many2one('nena.gen.status', string='Estatus SADA')
    notes = fields.Text(string='Regencia Notas')
    full_id_number = fields.Char(string='Cedula', compute='_compute_full_id_number', store=True)
    record_ids = fields.One2many('nena.record', 'regent_id', string='Expedientes Asociados')

    @api.depends('document_type_id.name', 'id_number')
    def _compute_full_id_number(self):
        for rec in self:
            if rec.document_type_id and rec.id_number:
                rec.full_id_number = f"{rec.document_type_id.name}{rec.id_number}"
            else:
                rec.full_id_number = ''