# -*- coding: utf-8 -*-
{
    'name': "nena_l10n_ve_tax_retention",
    'summary': "Tax Retention for Venezuela",
    'description': """
Retención de Impuestos IVA para Venezuela
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.1',
    'depends': ['base', 'account', 'nena_l10n_ve_tax_unit'],
    'data': [
        'security/ir.model.access.csv',
        #'data/l10n.ve.tax.retention.csv',
        'views/nena_l10n_ve_tax_retention_views.xml',
        'views/nena_l10n_tax_retention_menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}