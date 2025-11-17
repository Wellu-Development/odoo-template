{
    "name": "Nena Product",
    "summary": "Módulo custom que contiene la configuración de Producto",
    "author": "Droguería Nena, C.A.",
    "category": "Dronena",
    "version": "18.0.0.0.1",
    "application": True,
    "depends": [
        "base",
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product.category.csv",
        "views/product_category.xml",
        "views/nena_product_family.xml",
        "views/nena_product_class.xml",
    ],
}