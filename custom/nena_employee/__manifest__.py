{
    "name": "Nena Employee",
    "summary": "Modulos custom para Gestión de Empleados",
    "author": "Droguería Nena, C.A.",
    "category": "Dronena",
    "version": "18.0.0.0.1",
    "depends": ["base","hr"],
    "data": [
        "security/ir.model.access.csv",
        "data/hr.department.csv",
        "data/hr.job.csv",
        "views/hr_job.xml",
        "views/hr_employee.xml",
        "views/nena_config_collection_management.xml"
    ],
    "application": False,
    "license": "LGPL-3",
}