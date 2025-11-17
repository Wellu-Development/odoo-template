from odoo import models, fields, api

class NenaHrEmployee(models.Model):
    _inherit = "hr.employee"

    nena_config_collection_management_id = fields.Many2one("nena.config.collection.management", string="Disponilidad")

    #nena_zone_ids = fields.One2many("nena.zone", "nena_hr_employee_id", string="Zonas Asignadas")

    #nena_zone_ids = fields.One2many("nena.zone.assigment", "nena_hr_employee_id", string="Zonas Asignadas")

    nena_zone_ids = fields.Many2many("nena.zone", string="Zones")
    display_collection_management = fields.Boolean(default=True, store=True)


    @api.onchange('department_id')
    def _onchange_department(self):
        for record in self: 
            if record.department_id.nena_gen_category_id.code == 'COB':
                record.display_collection_management = False
            else:
                record.display_collection_management = True
