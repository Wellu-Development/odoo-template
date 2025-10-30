{
    "name": "Nena Partner Payment Type",
    "summary": "Customer payment Type",
    "description": "Customer payment Type: cash, credit, prepaid",
    "author": "Yenny Colmenarez",
    "category": "Uncategorized",
    "version": "18.0.0.0.4",
    "application": True,
    "depends": ["base"],
    "data": [
        "data/payment_types.xml",
        "security/ir.model.access.csv",
        "views/payment_type_views.xml",
        "views/menuitem.xml",
    ],
}
