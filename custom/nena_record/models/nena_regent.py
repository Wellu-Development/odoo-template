from odoo import models, fields,api

class NenaRegent(models.Model):
    _name = 'nena.regent'
    _description = 'Regent Data'

    document_type_id = fields.Many2one('nena.document.type', string='Document Type', required=True)
    id_number = fields.Char(string='ID Number', required=True)
    name = fields.Char(string='Regent Name', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Regent Address')

    matric_msds = fields.Char(string='MATRIC MSDS')
    colfar = fields.Char(string='COLFAR code')

    oper_min_start_date = fields.Date(string='Act. Start Date',required=True)
    oper_min_end_date = fields.Date(string='Act. End Date')

    inprefa_code = fields.Char(string='INPREFA Code')
    sicm_code = fields.Char(string='S.I.C.M Code',required=True)
    sicm_status = fields.Char(string='S.I.C.M Status')
    sada_code = fields.Char(string='SADA Code',required=True)
    sada_status = fields.Char(string='SADA Status')

    notes = fields.Text(string='Regency Notes')

    full_id_number = fields.Char(
        string='Full ID',
        compute='_compute_full_id_number',
        store=True
    )

    record_ids = fields.One2many(
    'nena.record',
    'regent_id',
    string='Expediente vinculado'
    )

    @api.depends('document_type_id.name', 'id_number')
    def _compute_full_id_number(self):
        for rec in self:
            if rec.document_type_id and rec.id_number:
                rec.full_id_number = f"{rec.document_type_id.name}{rec.id_number}"
            else:
                rec.full_id_number = ''