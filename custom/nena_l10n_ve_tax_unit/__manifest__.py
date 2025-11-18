# -*- coding: utf-8 -*-
{
    'name': "nena_l10n_ve_tax_unit",
    'summary': "Tributary Unit for Venezuela",
    'description': """
Unidad Tributaria para Venezuela
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.1',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/nena_l10n_ve_tax_unit_views.xml',  
        'views/fiscal_menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}