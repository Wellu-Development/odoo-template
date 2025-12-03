from odoo import models, fields

class DrugCompositionLine(models.Model):
    _name = 'nena.drug.composition.line'
    _description = 'Composition Line'

    composition_id = fields.Many2one('nena.drug.composition', string='Composition', required=True, ondelete='cascade')
    active_principle_id = fields.Many2one('nena.drug.active.principle', string='Active Principle', required=True)
    quantity = fields.Float(string='Amount', required=True)
    unit_id = fields.Many2one('uom.uom', string='Unit of Measurement', required=True)