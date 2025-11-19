from odoo import models, fields,api

class NenaPostulationMonitor(models.Model):
    _name = 'nena.postulation.monitor'
    _description = 'Postulation Monitor'

    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Expedientes') 
    monitor_ids = fields.One2many('nena.record', 'monitor_id') 
    name = fields.Char(string="Expediente", readonly="1")
    postulation_type = fields.Char(string="Tipo de Postulacion", readonly="1")
    purchases = fields.Boolean(string="Compras", readonly="1")
    sales = fields.Boolean(string="Ventas", readonly="1")
    regency = fields.Boolean(string="Regencia", readonly="1")
    legal = fields.Boolean(string="Juridica", readonly="1")
    payment = fields.Boolean(string="Cobranzas", readonly="1")

    @api.depends('monitor_ids') 
    def compute_stage(self): 
        if len(self.monitor_ids) > 0: 
            self.record_id = self.monitor_ids[0] 