# -*- coding: utf-8 -*-
# from odoo import http


# class CategoriaCliente(http.Controller):
#     @http.route('/categoria_cliente/categoria_cliente', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/categoria_cliente/categoria_cliente/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('categoria_cliente.listing', {
#             'root': '/categoria_cliente/categoria_cliente',
#             'objects': http.request.env['categoria_cliente.categoria_cliente'].search([]),
#         })

#     @http.route('/categoria_cliente/categoria_cliente/objects/<model("categoria_cliente.categoria_cliente"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('categoria_cliente.object', {
#             'object': obj
#         })

