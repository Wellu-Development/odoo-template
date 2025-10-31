from odoo import models, fields

class ResParnert(models.Model):
    _inherit = 'res.partner'
    
    person_type_id = fields.Many2one('tipo.persona', string='Tipo')

