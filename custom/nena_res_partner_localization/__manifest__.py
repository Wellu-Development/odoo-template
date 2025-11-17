# -*- coding: utf-8 -*-
{
    'name': "Nena Partner Localization VE",
    'summary': "Territorial political structure for Venezuela: State, Municipality, City",
    'description': """
Localización Territorial para Venezuela:
- Estados
- Municipios
- Ciudades
Integración con res.partner para direcciones localizadas.
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.2',
    'depends': [
        'base',
        'contacts',
        'base_address_extended'
    ],

    'data': [
        'security/ir.model.access.csv',

        # Vistas
        'views/nena_res_city_views.xml',
        'views/nena_res_country_municipality_views.xml',
        'views/nena_res_country_state_views.xml',
        'views/localization_menu_views.xml',

        # Datos
        'data/res.country.state.csv',
        'data/nena.res.country.municipality.csv',
        'data/res.city.csv'
    ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}