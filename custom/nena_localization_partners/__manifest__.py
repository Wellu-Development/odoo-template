# -*- coding: utf-8 -*-
{
    'name': "nena_localization_territorial_partners",
    'summary': "Politic Territorial for Venezuela",
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
        'views/nena_res_state_ve_views.xml',
        'data/nena.res.state.ve.csv',
        'views/nena_res_state_municipality_ve_views.xml',
        'data/nena.res.state.municipality.ve.csv',
        'views/nena_res_state_municipality_city_ve_views.xml',
        'data/nena.res.state.municipality.city.ve.csv',
    ]
}