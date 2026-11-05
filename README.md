# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador - Metodología de Sistemas II

## Descripción

Sistema de consola para administrar el ciclo de vida de trámites estudiantiles. Permite registrar solicitudes, asignar un responsable, cambiar su prioridad y estado, consultarlas y generar un reporte. El foco del trabajo es la mejora de la calidad interna: diagnóstico de deuda técnica, refactorings y pruebas automatizadas.

## Integrantes

- Facundo Gerbino
- Gonzalo Barrios
- Felipe Pozo

## Tecnologías Utilizadas

* Python 3.10+
* `dataclasses` y `Enum` para el modelo de dominio
* Persistencia simulada en memoria mediante `RepositorioSolicitudes`
* `unittest` para las pruebas automatizadas
* Sin dependencias externas

## Instalación y Ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/octantes/Trabajo-Final-Metodologias2-Barrios-Gerbino-Pozo.git
cd Trabajo-Final-Metodologias2-Barrios-Gerbino-Pozo
```

2. Ejecutar la demostración:

```bash
python3 main.py
```

## Pruebas

```bash
python3 -m unittest -v
```

Suite actual: 12 pruebas unitarias.

## Funcionalidades

1. Registrar una solicitud con datos validados y ID único.
2. Asignar un responsable.
3. Cambiar la prioridad (`BAJA`, `MEDIA`, `ALTA`).
4. Cambiar el estado (`PENDIENTE`, `EN_TRAMITE`, `RESUELTO`, `RECHAZADO`) respetando las transiciones permitidas.
5. Buscar una solicitud por ID y listar todas las solicitudes.
6. Generar un reporte por consola.

## Estructura

```text
sistema.py        Modelo de dominio, repositorio, reportes y gestor
main.py           Demostración ejecutable
test_sistema.py   Pruebas unitarias
docs/             Evidencias, checklist de code review y conclusiones
```

## Documentación

- [Evidencias y decisiones técnicas](docs/evidencias.md)
- [Checklist de code review](docs/checklist.md)
- [Conclusiones y mejoras futuras](docs/conclusiones.md)

## Tags

- `estado-inicial`: sistema base con los code smells
- `etapa-diagnostico`: diagnóstico de deuda técnica
- `etapa-refactoring`: refactorings aplicados
- `etapa-pruebas`: suite de pruebas
- `etapa-docs`: documentación final
- `estado-refactorizado`: estado final del código

## Repositorio

https://github.com/octantes/Trabajo-Final-Metodologias2-Barrios-Gerbino-Pozo