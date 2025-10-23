# -*- coding: utf-8 -*-
{
    'name': "nena_localization_tributary_unit_ve",
    'summary': "Tributary Unit for Venezuela",
    'description': """
Unidad Tributaria para Venezuela
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/l10n_ve_tax_unit_views.xml',  
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}