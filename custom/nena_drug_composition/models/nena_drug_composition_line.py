from odoo import models, fields

class DrugCompositionLine(models.Model):
    _name = 'nena.drug.composition.line'
    _description = 'Composición por principio activo'

    composition_id = fields.Many2one('nena.drug.composition', string='Composición', required=True, ondelete='cascade')
    active_principle_id = fields.Many2one('nena.drug.active.principle', string='Principio Activo', required=True)
    quantity = fields.Float(string='Cantidad', required=True)
    unit_id = fields.Many2one('uom.uom', string='Unidad de Medida', required=True)

    # quantity_jar = fields.Float(string='Cantidad', required=True)
    # unit_jar_id = fields.Many2one('uom.uom', string='Unidad de Medida', required=True)
