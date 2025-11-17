from odoo import models, fields

class NenaGenCategoryInheritance(models.Model):
    _inherit = "nena.gen.category"

    departaments_ids = fields.One2many("hr.department", "nena_gen_category_id", string="Departamentos")