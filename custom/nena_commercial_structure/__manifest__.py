# -*- coding: utf-8 -*-
{
    'name': "Nena Estructura Comercial",
    'summary': "Estructura comercial de Nena",
    'description': """
    Estructura comercial de Nena
    """,
    'author': "César Enrique",
    'category': 'Uncategorized',
    'version': '18.0.0.0.1',
    'depends': ['base', "contacts"],
    'data': [
        'security/ir.model.access.csv',
        'views/commercial_structure_views.xml',
        'views/menuitem.xml'
    ],
    'application': True
}