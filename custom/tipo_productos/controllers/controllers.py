# -*- coding: utf-8 -*-
# from odoo import http


# class TipoProductos(http.Controller):
#     @http.route('/tipo_productos/tipo_productos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tipo_productos/tipo_productos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tipo_productos.listing', {
#             'root': '/tipo_productos/tipo_productos',
#             'objects': http.request.env['tipo_productos.tipo_productos'].search([]),
#         })

#     @http.route('/tipo_productos/tipo_productos/objects/<model("tipo_productos.tipo_productos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tipo_productos.object', {
#             'object': obj
#         })

