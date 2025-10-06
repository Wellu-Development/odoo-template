# ARQUITECTURA BASE PARA PROYECTOS BASADOS EN ODOO

config/ -> Archivos de configuración del proyecto. (odoo.conf, entre otros...)

custom/ -> Directorio con los modulos custom del proyecto, los mismos llevan como prefijo el nombre del cliente, por ejemplo "digitel_account"

enterprise/ -> Directorio con los modulos enterprise de odoo en el caso de hacer uso de los mismos, en caso contrario solo se borra este directorio

internal/ -> Directorio con los modulos base predesarrollados para ser reutilizados en distintos proyectos, los mismos llevan como prefijo el nombre de tu empresa, por ejemplo "google_crm"

third_party/ -> Directorio con los modulos de terceros que deban ser integrados, estos no llevan ningun prefijo y se suben con el mismo nombre tecnico que traigan

.env.example -> Variables de entorno necesarias para levantar el proyecto (cambiarle el nombre a .env)

Dockerfile -> Cambiar la version en el FROM en caso de requerir una version distinta de odoo
