# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/custom-addons/nen/nenaLocalizationPartners(http.Controller):
#     @http.route('//mnt/custom-addons/nen/nena_localization_partners//mnt/custom-addons/nen/nena_localization_partners', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/custom-addons/nen/nena_localization_partners//mnt/custom-addons/nen/nena_localization_partners/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/custom-addons/nen/nena_localization_partners.listing', {
#             'root': '//mnt/custom-addons/nen/nena_localization_partners//mnt/custom-addons/nen/nena_localization_partners',
#             'objects': http.request.env['/mnt/custom-addons/nen/nena_localization_partners./mnt/custom-addons/nen/nena_localization_partners'].search([]),
#         })

#     @http.route('//mnt/custom-addons/nen/nena_localization_partners//mnt/custom-addons/nen/nena_localization_partners/objects/<model("/mnt/custom-addons/nen/nena_localization_partners./mnt/custom-addons/nen/nena_localization_partners"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/custom-addons/nen/nena_localization_partners.object', {
#             'object': obj
#         })

