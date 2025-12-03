{
    "name": "Nena Accounting",
    "summary": "Modulos custom para Finanzas",
    "author": "Droguería Nena, C.A.",
    "category": "Dronena",
    "version": "18.0.0.0.1",
    "depends": [
        "base",
        "accountant",
        "nena_general_parameter"
        ],
    "data": [
        "security/ir.model.access.csv",
        "data/nena.payment.type.csv",
        "data/account.payment.term.csv",
        "views/nena_payment_type.xml",
        "views/nena_credit_conditions.xml",
    ],
    "application": False,
    "license": "LGPL-3",
}