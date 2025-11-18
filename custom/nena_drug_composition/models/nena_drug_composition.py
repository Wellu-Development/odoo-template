from odoo import models, fields

class DrugComposition(models.Model):
    _name = 'nena.drug.composition'
    _description = 'Drug Composition'

    reference = fields.Char(string='Reference', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    line_ids = fields.One2many('nena.drug.composition.line', 'composition_id', string='Principios Activos')

    presentation_id = fields.Many2one('nena.prod.presentation', string='Presentación', required=True)
    has_dosage = fields.Boolean(
        related='presentation_id.has_dosage', store=True, string='Presentacion tiene dosificación')
    #Para mostrar estos campos simplemente el campo de has_dosage debe ser True
    dosage_amount = fields.Float(string='Cantidad de Dosificación')
    dosage_unit = fields.Many2one('uom.uom', string='Unidad de Dosificación')