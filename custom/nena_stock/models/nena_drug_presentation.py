from odoo import models, fields

class DrugPresentation(models.Model):
    _name = 'nena.drug.presentation'
    _description = 'Presentation'
    _rec_name = 'abbrev_presentation'

    reference = fields.Char(string='Reference')
    abbrev_presentation = fields.Char(string='Abbreviated Presentation', size=10)
    description_presentation = fields.Char(string='Presentation Description', size=100)
    has_dosage = fields.Boolean(string='It has a Dosage', default=False)
    uom_presentation_id = fields.Many2one('uom.uom', string='Unit of Measurement')
    active = fields.Boolean(string='Active', default=True)