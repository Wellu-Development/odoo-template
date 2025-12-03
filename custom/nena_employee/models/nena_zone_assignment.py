from odoo import models, fields

class NenaZoneAssignment(models.Model):
    _name = 'nena.zone.assigment'
    _description = 'Zone Assignment'

    hr_employee_id = fields.Many2one("hr.employee", string="Employee")
    zone_ids = fields.Many2many("nena.zone", string="Zones")