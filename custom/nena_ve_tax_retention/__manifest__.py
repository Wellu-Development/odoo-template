# -*- coding: utf-8 -*-
{
    'name': "nena_localization_tax_retention_ve",
    'summary': "Tax Retention for Venezuela",
    'description': """
Retención de Impuestos IVA para Venezuela
    """,
    'author': "Dronena",
    'website': "",
    'category': 'Localization',
    'version': '18.0.0.0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_ve.tax.retention.csv',
        'views/nena_tax_retention_ve_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}