# Guía general para trabajar con GIT

Este documento resume las guías ofigenerales para estructurar un flujo de trabajo profesion en cualquier controlador de versiones que utilice GIT como base.

## Configuración de usuario GIT

* git config --global user.name "John Doe"
* git config --global user.email "john.doe@gmail.com"

**Estructura del commit**:

| Título                   | Descripción                                                                                |
| :----------------------- | :----------------------------------------------------------------------------------------- |
| `Etiqueta`               | Es un prefijo que permite identificar el comportamiento de un commit.                      |
| `Módulo`                 | Es el nombre técnico del módulo que se esta afectando.                                     |
| `Descripción corta`      | Es la descripción principal del commit, permite conocer el objetivo de este.               |
| `Descripción completa`   | Contiene los detalles del trabajo realizado sobre el módulo.                               |

**Ejemplo**:

```
[ETIQUETA] nombre_modulo: Descripción corta debe ser menor a 50 caracteres
```

**Tipos de etiquetas**:

| Nombre   | Descripción                                                                                     |
| :------- | :---------------------------------------------------------------------------------------------- |
| `[FIX]`  | Se utiliza para corrección de errores.                                                          |
| `[REF]`  | Se utiliza para refactorización.                                                                |
| `[ADD]`  | Se utiliza para agregar nuevas funcionalidades al módulo.                                       |
| `[REM]`  | Se utiliza para eliminar recursos: eliminar código inactivo, eliminar vistas, eliminar módulos. |
| `[REV]`  | Se utiliza para revertir commits anteriores.                                                    |
| `[MOV]`  | Se utiliza para mover archivos o bloques de codigo entre archivos.                              |
| `[REL]`  | Se utiliza para commits de despliegues a produccion.                                            |
| `[IMP]`  | Se utiliza para mejoras realizadas.                                                             |
| `[MERGE]`| Se utiliza para commits que confirmen un Merge de forma local.                                  |
| `[CLA]`  | Se utiliza para firma de licencia como colaborador oficial de Odoo.                             |
| `[I18N]` | Se utiliza para cambios en archivos de traduccion.                                              |

**Nombre de módulo**:

Se refiere al nombre técnico del módulo que se esta modificando. Se recomienda que un commit NO contenga cambios simultaneos hacia varios módulos, si no mas bien que los cambios esten asociados a un único módulo.

**Descripción corta**:

Debe explicar por si mismo el motivo del cambio, NO puede ser ambiguo como por ejemplo “correccion de errores“ o “mejoras“. Se debe limitar la longitud del mensaje, esta no debe ser mayor a 50 caracteres.

Se sugiere completar la siguiente oración para poder definir un buen mensaje corto: “si se aplica, este commit“
Ejemplo: “si se aplica, este commit evitará archivar usuarios vinculados a partners activos“

En este caso nos quedaremos con la oracion construida luego de la palabra commit, quedaria lo siguiente: evitará archivar usuarios vinculados a partners activos.

Por lo que el encabezado del commit quedara de esta manera:
[IMP] nena_partner: evitar archivar usuarios vinculados a partners activos.

**Descripción completa**:

En esta descripción se debe ampliar el nivel de detalles, indicando especificamente el archivo que se esta editando y la funcion o método que se esta modificando indicando el POR QUE se esta haciendo esa modificación en el código. De este modo aseguramos que la descipción perdure en el tiempo, es decir, que si dentro de 4 años llega algun miembro nuevo al equipo, este pueda leer el commit y entenderlo de manera sencilla.
Por su parte es importante incluir todos los recursos externos que se utilizaron para llevar a cabo los cambios indicados en la descripcion del commit, por ejemplo: “Se utilizo la libreria python paramiko en su version 1.5“, “Se implemento una libreria externa llamada chart.js para implementar desarrollo de interfaces dinámicas“.

## Estructura del Pull Request

Es importante tomarse el tiempo para poder generar un buen commit, con el suficiente nivel de información que pueda justificar su aprobacion en el Pull Request, por lo tanto se recomienda que si alguna tarea carece de sentido, propósito o especificaciones, entonces es mejor detenerse hasta aclarar dicho propósito con la persona que corresponda y luego de esto si poder continuar con el desarrollo de la tarea.

| PR                     | Descripción                                                                                           |
| :--------------------- | :---------------------------------------------------------------------------------------------------- |
| `Título`               | Se combina el numero identificado del ticket o requerimiento mas el titulo de la tarea asignada.      |
| `Descripción completa `| Debe indicar el POR QUE se esta generando este PR y cual es el motivo especifico que justifica el PR. |