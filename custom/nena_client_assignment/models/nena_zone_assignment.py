from odoo import models, fields

class NenaZoneAssignment(models.Model):
    _name = 'nena.zone.assigment'
    _description = 'Asignación de Zonas'

    nena_hr_employee_id = fields.Many2one("hr.employee", string="Employee")
    #nena_zone_id = fields.Many2one("nena.zone", string="Zona Asignado")
    nena_zone_ids = fields.Many2many("nena.zone", string="Zones")