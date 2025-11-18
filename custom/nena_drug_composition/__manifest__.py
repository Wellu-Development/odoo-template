{
    'name': 'Drug Composition',
    'version': '18.0.0.0.1',
    'summary': 'Manage pharmaceutical compositions linked to products',
    'description': """
                    Este módulo permite definir los principios activos y las composiciones 
                    de los productos farmacéuticos, vinculándolos directamente al modelo 
                    de producto nativo en Odoo.
""",
    'author': 'Angel Manzano',
    'category': 'Inventory',
    'depends': ['product', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/active_principle_views.xml',
        'views/composition_views.xml',
        'views/prod_presentation_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
