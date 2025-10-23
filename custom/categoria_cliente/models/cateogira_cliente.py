from odoo import models, fields

class CategoriaCliente(models.Model):
    _name = 'categoria.cliente'
    _description = 'Categoría de Cliente'

    codCategoria = fields.Char(string='Codigo de la Categoría', required=True)
    nombre = fields.Text(string='Nombre')
    nomedicina = fields.Boolean(string='NoMedicina')
    websiteavaible = fields.Boolean(string='WebSite')
    tipo_producto_id = fields.Many2one('tipo.producto')
    active = fields.Boolean(string='Activo')
