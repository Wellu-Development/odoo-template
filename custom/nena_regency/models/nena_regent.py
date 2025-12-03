from odoo import models, fields,api

class NenaRegent(models.Model):
    _name = 'nena.regent'
    _description = 'Regent'

    document_type_id = fields.Many2one('nena.type.identification', string='Document Type', required=True)
    id_number = fields.Char(string='ID Number', required=True)
    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    matric_msds = fields.Char(string='MATRIC MSDS')
    colfar = fields.Char(string='COLFAR')
    inprefa_code = fields.Char(string='INPREFA')
    oper_min_start_date = fields.Date(string='From Func. Act.',required=True)
    oper_min_end_date = fields.Date(string='Until Func. Act')
    sicm_code = fields.Char(string='S.I.C.M. Code',required=True)
    sicm_status_id = fields.Many2one('nena.gen.status', string='S.I.C.M. Status')
    sada_code = fields.Char(string='SADA Code',required=True)
    sada_status_id = fields.Many2one('nena.gen.status', string='SADA Status')
    notes = fields.Text(string='Regency Notes')
    full_id_number = fields.Char(string='ID Card', compute='_compute_full_id_number', store=True)

    @api.depends('document_type_id.name', 'id_number')
    def _compute_full_id_number(self):
        for rec in self:
            if rec.document_type_id and rec.id_number:
                rec.full_id_number = f"{rec.document_type_id.name}{rec.id_number}"
            else:
                rec.full_id_number = ''