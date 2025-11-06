from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Expedientes') 
    res_partner_ids = fields.One2many('nena.record', 'res_partner_id') 

    @api.depends('res_partner_ids') 
    def compute_stage(self): 
        if len(self.res_partner_ids) > 0: 
            self.record_id = self.res_partner_ids[0] 