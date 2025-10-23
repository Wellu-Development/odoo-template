{
    "name": "Nena Postulaciones",
    "summary": "Módulo Web de Postulaciones",
    "author": "Jose Acosta",
    "category": "Website",
    "version": "18.0.0.0.2",
    "application": True,
    "depends": ["contacts", "web", "website", "base_address_extended", "mail"],
    "data": ["views/client_postulation_template.xml"],
    "assets": {
        "web.assets_frontend": [
            "nena_postulation/static/src/components/**/*.js",
            "nena_postulation/static/src/components/**/*.xml",
        ]
    },
}
