from odoo import models, fields

class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'

    ref = fields.Char(string='Referencia')