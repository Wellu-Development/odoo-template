{
    "name": "Nena Product",
    "summary": "Módulo custom que contiene la configuración de Producto",
    "author": "Droguería Nena, C.A.",
    "category": "Dronena",
    "version": "18.0.0.0.1",
    "application": False,
    "depends": [
        "base",
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product.category.csv",
        "data/nena.product.subtype.csv",
        "data/product_family.xml",
        "data/product_class.xml",
        "views/product_category.xml",
        "views/product_subtype.xml",
        "views/nena_product_family.xml",
        "views/nena_product_class.xml",
        "views/menu_stock.xml",
    ],
}