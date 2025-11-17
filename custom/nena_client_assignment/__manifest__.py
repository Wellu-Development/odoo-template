{
    "name": "Nena Asignación de Clientes",
    "summary": "Módulo de Asignación de Clientes",
    "author": "Jose Alvarez",
    "category": "Uncategorized",
    "version": "18.0.0.0.2",
    "application": True,
    "depends": ["base","hr","nena_partner_config_record","nena_record"],
    "data": [
        "security/ir.model.access.csv",
        'views/nena_hr_job_views.xml',
        'views/nena_hr_department_views.xml',
        'views/nena_hr_employee_views.xml',
        'views/nena_config_collection_management_views.xml',   
        'views/nena_hr_views.xml'
    ],
    'installable': True,
    'auto_install': False
}
