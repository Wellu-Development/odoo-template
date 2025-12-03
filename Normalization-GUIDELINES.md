# Guía de Normalizacion para Desarrollo en Odoo de Dronena

Este documento establece las reglas y directrices para garantizar la uniformidad, claridad y mantenibilidad del código, asi como tambien la estructura de archivos en todo nuestro proyecto.

Nos centraremos específicamente en:
- Las convenciones de nombres para directorios (carpetas) y modelos (_name).
- El contenido esencial de cada nuevo módulo que se cree.

## 🛠️ Estandarización del Entorno (Visual Studio Code)

Para asegurar la uniformidad en el estilo de codificación (principalmente Python) y acelerar el desarrollo, es obligatorio que todos los miembros del equipo instalen y utilicen las siguientes extensiones en su entorno de Visual Studio Code:

| Extensión | Propósito | Descripción |
| :----------------- | :-------------------------- | :---------------------------------------------------------------------------------- |
| Black Formatter | Formateo de Código Python | Aplicación automática de los estándares de formato PEP 8. |
| Odoo Snippets | Fragmentos de Código XML | Provee atajos y snippets para estructuras comunes en vistas y archivos XML de Odoo. |
| Odoo Code Snippets | Fragmentos de Código Python | Provee atajos y snippets para estructuras comunes en modelos y métodos de Odoo. |

## 📂 Convenciones de Nombres

La consistencia en los nombres es fundamental para la navegabilidad y comprensión del proyecto.

🐍 Nombres de Directorios (Módulos)

El nombre del directorio raíz del módulo debe comenzar con el prefijo `nena_` seguido de la palabra clave que define el proceso o dominio de negocio. El resto del nombre debe ser funcional, todo en minúsculas y separando palabras con guiones bajos (`_`).

Tabla de Mapeo de Procesos y Prefijos de Carpeta:

| Proceso | Prefijo de Carpeta Estándar | Descripción y Regla de Dependencia |
| :------------------------------- | :------------------- | :------------------------------- |
| Parámetros Generales | `nena_general_parameter` | Módulo de Configuración. Contiene modelos de configuración, parámetros, o listas maestras que son utilizados por otros procesos. Este módulo no debe depender de ningún otro |
| Expedientes Clientes / Proveedor | `nena_partner_record` |
| Empleados | `nena_employee` |
| Ventas | `nena_sales` |
| Compras | `nena_purchasing` |
| Almacén | `nena_stock` |
| Finanzas | `nena_accounting` |
| Regencia | `nena_regency` |
| Promociones | `nena_promotion` |

**Directriz de Asignación de Módulos (Obligatoria):** Cualquier nuevo módulo o funcionalidad debe ser creado obligatoriamente dentro de alguna de las carpetas de proceso ya definidas en la tabla anterior. Si durante el desarrollo surge la necesidad de un nuevo proceso o dominio de negocio que no encaja en las categorías existentes, la creación de una nueva carpeta de proceso (`nena_nuevo_proceso`), requerirá la aprobación y acuerdo formal de todo el equipo de desarrollo.

**Regla de Dependencias:** Al asignar un módulo a una carpeta, se debe evitar la creación de dependencias circulares. Un módulo en una carpeta de un dominio superior (que contiene módulos genéricos o de base) nunca debe depender de un módulo que se encuentre en una carpeta de un dominio inferior (más específico).

🐍 Nombres de Modelos (`_name`)

El atributo `_name` del modelo en Python debe seguir la siguiente estructura:

| Tipo | Uso | Formato | Ejemplo |
| :---------------- | :---------------------------------------------------------------- | :------------------- | :------------------------------ |
| Modelos Nuevos | Para cualquier modelo que se crea desde cero. | `nena.nombre.modelo` | `nena.sale.order.line.discount` | 
| Modelos Heredados | Para modelos que extienden o modifican modelos existentes de Odoo | Sin Prefijo | `sale.order`, `res.partner` |

**Regla Clave:** Solo se utiliza el prefijo `nena.` para modelos totalmente nuevos. Si el objetivo es modificar un modelo ya existente de Odoo, se debe usar el nombre original de dicho modelo sin el prefijo `nena.`.

## 📄 Estructura y Contenido del Archivo `__manifest__.py`

El archivo manifiesto es la identidad de nuestro módulo. Debe ser claro, completo y sus elementos deben estar ordenados para asegurar una carga correcta.

`name`: Nombre descriptivo, breve y legible por el usuario (ej: "Mejoras en Descuentos de Ventas").
`summary`: Breve descripcion de la función de módulo.
`author`: Droguería Nena, C.A.
`category`: Dronena
`version`: Seguir el estándar de versionamiento interno del equipo, actualmente "18.0.0.0.1".
`depends`: Lista completa de todos los módulos Odoo de los que depende (ej: ['base', 'sale']).
`data`: Lista de archivos XML/CSV que deben ser cargados por Odoo, ordenados por prioridad de carga (seguridad, data, vistas).
`assets`: Declara los archivos estáticos (JavaScript, CSS, SCSS, QWeb) necesarios para el módulo.
`application`: Indica si el módulo representa una aplicación completa o un módulo técnico.
`license`: Tipo Licencia asociado al Producto, por defecto "LGPL-3"

## 🛠️ Extensión de la Estructura del Módulo

Para una mejor organización y separación de las vistas frontend y backend, se va trabajar con el directorio `templates/`, con el proposito de alojar todos los archivos XML (Vistas QWeb) que definan plantillas para el Portal Web, el Sitio Web (website) o cualquier otra vista orientada al frontend.