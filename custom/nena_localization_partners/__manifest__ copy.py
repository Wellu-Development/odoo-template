# -*- coding: utf-8 -*-
{
    'name': "nena_localization_partners",
    'summary': "Localización Política Territorial NENA",
    'description': """
Localización Territorial: Estado - Municipio - Parroquia - Ciudad
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.1',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/nena_localization_partner_state_ve.csv',
        'data/nena_localization_partner_municipality_ve.csv',
        'data/nena_localization_partner_city_ve.csv',
        'views/nena_res_state_ve_views.xml',
        'views/nena_res_state_municipality_ve_views.xml',
        'views/nena_res_state_municipality_city_ve_views.xml',
        'views/res_partner_views.xml',
    ]
}