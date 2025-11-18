from odoo import models, fields, api 

class NenaGenManagement(models.Model):
    _name = "nena.gen.management"
    _description = "General Management"
    _rec_name = "name"
    
    code = fields.Char(string="Codigo", required=True)
    name = fields.Char(string="Descripción", required=True)
    parent_id = fields.Many2one('nena.gen.management', string='Tipo de Gestión', index=True, ondelete='restrict')
    child_ids = fields.One2many('nena.gen.management', 'parent_id', string='Hijos')
    department = fields.Boolean(string="Departamentos")