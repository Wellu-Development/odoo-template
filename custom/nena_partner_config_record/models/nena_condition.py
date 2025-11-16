from odoo import models, fields, api

class NenaCondition(models.Model):
    _name = "nena.condition"
    _description = "Condition"
    _rec_name = "description"
    
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "El Codigo debe ser único.",
        ),
        (
            "description_management_unique",
            "UNIQUE(description, gen_management_id)",
            "La combinación de descripción y tipo de gestion debe ser única.",
        )
    ]

    code = fields.Char(string='Código', readonly=True, copy=False, default='000')
    description = fields.Char(string="Descripcion", required=True)
    ref = fields.Integer(string="Referencia")
    gen_management_id = fields.Many2one('nena.gen.management', string="Tipo de Gestión", required=True)

    @api.model
    def create(self, vals):
        sequence = self.env.ref('nena_condition.seq_nena_condition_code')
        sequence.number_next = 55  # O el número correcto

        if vals.get('code', '000') == '000':
            vals['code'] = self.env['ir.sequence'].next_by_code('nena.condition.code') or '000'
        return super(NenaCondition, self).create(vals)