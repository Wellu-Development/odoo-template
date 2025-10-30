{
    "name": "Nena Record",
    "summary": "Módulo custom que contiene la información del Expediente",
    "author": "Anais Chavez",
    "category": "Uncategorized",
    "version": "18.0.0.0.1",
    "application": True,
    "depends": [
        "base",
        "contacts",
        "nena_localization_partners",
        "l10n_ve_ut"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/nena.region.csv",
        "data/nena.district.csv",
        "data/nena.zone.csv",
        "views/record.xml",
        "views/availability.xml",
        "views/group.xml",
        "views/chain.xml",
        "views/commercial_structure.xml",
        'views/nena_chain_credit_conditions.xml',
        'views/nena_client_credit_conditions.xml',
        'views/nena_credit_conditions.xml',
        "views/menuitem.xml",
    ],
}
