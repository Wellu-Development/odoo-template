{
    'name': 'Nena Drug Composition',
    'summary': 'Manage pharmaceutical compositions linked to products',
    'author': 'Droguería Nena, C.A.',
    'category': 'Inventory',
    'version': '18.0.0.0.1',
    'application': False,
    'description': 
                """
                    Este módulo permite definir los principios activos y las composiciones 
                    de los productos farmacéuticos, vinculándolos directamente al modelo 
                    de producto nativo en Odoo.
                """,
    'depends': ['product', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/active_principle_views.xml',
        'views/composition_views.xml',
        'views/prod_presentation_views.xml',
    ],
}