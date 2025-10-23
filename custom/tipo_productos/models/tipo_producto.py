from odoo import models, fields

class TipoProducto(models.Model):
    _name = 'tipo.producto'
    _description = 'Tipo de Producto'
    _rec_name = "valor"
    
    idn = fields.Integer(string='Identificador del Tipo de Producto', required=True)
    valor = fields.Text(string='Valor')

