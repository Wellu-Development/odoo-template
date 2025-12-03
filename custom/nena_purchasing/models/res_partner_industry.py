from odoo import models, fields

class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'

    ref_nena = fields.Char(string='Reference')