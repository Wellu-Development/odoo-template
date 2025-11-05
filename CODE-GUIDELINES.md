# Guías de Código Odoo

Este documento resume las guías oficiales de codificación de Odoo para estructura de módulos, nombrado de archivos y formato XML.

## 📂 Estructura del Módulo

Organiza tu módulo en estos directorios principales:

| Directorio   | Propósito |
| :----------- | :----------------------------------------------------------------------------------------- |
| `models/`    | Contiene archivos Python para definiciones de modelos. |
| `views/`     | Contiene archivos XML para vistas y plantillas del backend. |
| `data/`      | Contiene archivos XML para datos de demostración y datos reales. |
| `security/`  | Contiene archivos para permisos (`ir.model.access.csv`), grupos y reglas de registros. |
| `controllers/`| Contiene archivos Python para controladores HTTP. |
| `static/`    | Contiene recursos web (JS, CSS, imágenes), normalmente dentro de subdirectorios `src/` y `lib/`. |
| `wizard/`    | Contiene modelos transitorios (`models.TransientModel`) y sus vistas. |
| `report/`    | Contiene modelos y plantillas para reportes imprimibles y reportes basados en SQL. |
| `tests/`     | Contiene pruebas en Python. |

**Ejemplo de estructura de directorios**:
```
addons/plants/
├── manifest.py
├── controllers/
│ ├── init.py
│ └── plants.py
├── data/
│ └── plants.xml
├── models/
│ ├── init.py
│ └── plants.py
├── security/
│ └── ir.model.access.csv
├── static/
│ └── src/
│ ├────── js/
│ └────── scss/
└── views/
└────── plants.xml
```

## 📝 Convenciones de Nombrado de Archivos

Usa nombres significativos con solo caracteres `[a-z0-9_]` (letras minúsculas, números y guión bajo).

| Componente | Patrón de Nombrado | Ejemplo |
| :--------------- | :------------------------------------------------------- | :------------------------------------------- |
| **Modelos** | Nombre del modelo principal. Modelos heredados en archivos separados. | `plants.py`, `res_partner.py` |
| **Seguridad** | Grupos, reglas de registros. | `plants_groups.xml`, `security_plants.xml` |
| **Vistas** | Vistas del backend, menús, plantillas QWeb. | `plants.xml`, `plants_templates.xml` |
| **Datos** | Archivos de datos o demostración por modelo. | `plants.xml`, `plants_demo.xml` |
| **Controladores** | Archivo del controlador principal nombrado como el módulo. | `plants.py` |
| **Asistentes** | Modelos transitorios y vistas en directorio `wizard/`. | `order_plants.py`, `order_plants.xml` |

## 📄 Directrices de Formato XML

- **Usar notación `<record>`**: Colocar el atributo `id` antes de `model`. Para las etiquetas field, el atributo `name` debe ir primero.
- **Usar etiquetas abreviadas**: Preferir etiquetas como `<menuitem>` y `<template>` sobre la notación genérica `<record>` cuando estén disponibles.
- **Agrupar registros**: Intentar agrupar registros por modelo. Usar la etiqueta `<data>` solo para establecer datos noupdate.
- **Nombrado para XML IDs**:
  - **Menú**: `<model_name>_menu`
  - **Vista**: `<model_name>_view_<tipo_vista>` (ej: `tipo_vista` es `kanban`, `form`, `list`).
  - **Acción**: `<model_name>_action`.

**Ejemplo de un registro XML bien formateado**:
```xml
<record id="vista_id" model="ir.ui.view">
    <field name="name">nombre.vista</field>
    <field name="model">nombre_objeto</field>
    <field name="priority" eval="16"/>
    <field name="arch" type="xml">
        <tree>
            <field name="mi_campo_1"/>
            <field name="mi_campo_2" string="Mi Etiqueta" widget="statusbar"/>
        </tree>
    </field>
</record>
```


🐍 Directrices de Python (Resumen)
Estructura de Importaciones
```py
#### 1. Librerías estándar de Python

import logging
from datetime import datetime

#### 2. Librerías de terceros
from dateutil.relativedelta import relativedelta

#### 3. Importaciones de Odoo
from odoo import models, fields, api
from odoo.exceptions import UserError
```

Modelos y Métodos
```py
class ModeloEjemplo(models.Model):
    _name = 'modelo.ejemplo'
    _description = 'Modelo de Ejemplo'
    
    campo_ejemplo = fields.Char(string='Campo Ejemplo')
    
    @api.depends('campo_relacionado')
    def _compute_campo_calculado(self):
        for registro in self:
            registro.campo_calculado = registro.campo_relacionado * 2
    
    @api.constrains('campo_importante')
    def _check_campo_importante(self):
        for registro in self:
            if not registro.campo_importante:
                raise ValidationError(_("El campo importante es requerido"))
```

📜 Directrices de JavaScript (Resumen)
Estructura de Componentes

```js
/** @odoo-module */

import { Component, useState } from "@odoo/owl";

export class WidgetPersonalizado extends Component {
    static template = "nombre_modulo.WidgetPersonalizadoTemplate";
    static props = {
        record: Object,
    };

    setup() {
        this.state = useState({
            valor: this.props.record.data.valor,
        });
    }

    onClickBoton() {
        // Lógica del evento
    }
}
```

🔤 Convenciones de Nombrado
Python: snake_case para variables y métodos, PascalCase para clases

JavaScript: camelCase para variables y funciones, PascalCase para componentes

Archivos: snake_case para todos los archivos.

para mayor nivel de detalle consultar https://www.odoo.com/documentation/19.0/es_419/contributing/development/coding_guidelines.html