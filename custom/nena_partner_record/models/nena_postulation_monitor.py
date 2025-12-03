from odoo import models, fields, api

class NenaPostulationMonitor(models.Model):
    _name = 'nena.postulation.monitor'
    _description = 'Postulation Monitor'

    name = fields.Char(string="Record")
    postulation_type = fields.Char(string="Postulation Type")
    purchase = fields.Boolean(string="Purchase")
    sales = fields.Boolean(string="Sales")
    regency = fields.Boolean(string="Regency")
    legal = fields.Boolean(string="Legal")
    payment = fields.Boolean(string="Payment")
    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Records') 
    monitor_ids = fields.One2many('nena.record', 'monitor_id') 

    @api.depends('monitor_ids') 
    def compute_stage(self): 
        if len(self.monitor_ids) > 0: 
            self.record_id = self.monitor_ids[0] 