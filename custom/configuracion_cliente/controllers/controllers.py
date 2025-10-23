# -*- coding: utf-8 -*-
# from odoo import http


# class ConfiguracionCliente(http.Controller):
#     @http.route('/configuracion_cliente/configuracion_cliente', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/configuracion_cliente/configuracion_cliente/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('configuracion_cliente.listing', {
#             'root': '/configuracion_cliente/configuracion_cliente',
#             'objects': http.request.env['configuracion_cliente.configuracion_cliente'].search([]),
#         })

#     @http.route('/configuracion_cliente/configuracion_cliente/objects/<model("configuracion_cliente.configuracion_cliente"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('configuracion_cliente.object', {
#             'object': obj
#         })

