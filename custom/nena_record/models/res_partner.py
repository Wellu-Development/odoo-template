from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Expedientes') 
    res_partner_ids = fields.One2many('nena.record', 'res_partner_id') 
    person_type_id = fields.Many2one('nena.person.type', string='Tipo de Contacto')
    rif_type_id = fields.Many2one('nena.document.type', string='RIF')
    rif_number = fields.Char(string="Número RIF", size=9, required=True)