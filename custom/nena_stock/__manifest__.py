{
    "name": "Nena Stock",
    "summary": "Modulos custom para Inventario",
    "author": "Droguería Nena, C.A.",
    "category": "Dronena",
    "version": "18.0.0.0.1",
    "depends": [
        "base",
        "stock",
        "product", 
        "uom"
        ],
    "data": [
        "security/ir.model.access.csv",
        "data/product.category.csv",
        "data/nena.product.subtype.csv",
        "views/product_category.xml",
        "views/nena_product_subtype.xml",
        "views/nena_product_family.xml",
        "views/nena_product_class.xml",
        "views/nena_drug_active_principle.xml",
        "views/nena_drug_composition.xml",
        "views/nena_drug_presentation.xml",
        "views/product.xml",
        ],
    "application": False,
    "license": "LGPL-3",
}