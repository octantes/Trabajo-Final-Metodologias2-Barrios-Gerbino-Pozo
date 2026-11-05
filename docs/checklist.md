# Checklist de Code Review

**Alcance revisado:** `sistema.py`, `main.py`, `test_sistema.py`.
**Commit revisado:** `8bf0e88` (`fix: unificar errores de dominio y ampliar pruebas`).
**Fecha:** 2026-11-05.

## Evidencia de ejecución

```text
$ python3 -m unittest -v
Ran 19 tests in 0.001s
OK

$ python3 main.py
(salida del reporte)
EXIT=0
```

## Checklist técnico

| Área | Criterio | Resultado | Observación |
|---|---|---|---|
| Nombres | Nombres descriptivos y del dominio | ✅ | Se eliminaron `lista_sol`, `req`, `s` e `id_sol`; se usan `solicitud`, `id_solicitud` y `DatosNuevaSolicitud`. |
| Funciones | Funciones acotadas y con una responsabilidad | ✅ | El gestor orquesta; el repositorio almacena; el generador imprime. |
| SRP | Cada clase tiene un motivo claro para cambiar | ✅ | `Solicitud`, `RepositorioSolicitudes`, `GeneradorReportes` y `GestorSolicitudes` están separados. |
| OCP | Las transiciones se extienden sin modificar `if-elif` centrales | ✅ | `Solicitud` usa el mapa `_transiciones_permitidas`. |
| LSP | Los subtipos respetan el contrato de la base | No aplica | No se introdujeron jerarquías de herencia; no hay contratos de sustitución que validar. |
| ISP | No se obliga a depender de operaciones que no se usan | ✅ | Almacenamiento y presentación quedaron en componentes separados. |
| Manejo de errores | No hay errores silenciosos ni retornos ambiguos | ✅ | Se usan `SolicitudNoEncontradaError`, `TransicionInvalidaError`, `EstadoInvalidoError`, `DatosInvalidosError` y `SolicitudDuplicadaError`. |
| Validación | Los datos inválidos no llegan al dominio | ✅ | `DatosNuevaSolicitud.__post_init__` valida ID, estudiante, textos y prioridad. |
| Duplicados | No se admiten IDs repetidos | ✅ | `RepositorioSolicitudes.agregar` lanza `SolicitudDuplicadaError`. |
| Duplicación | La búsqueda por ID no está repetida | ✅ | Está centralizada en `obtener_por_id`. |
| Pruebas | Los flujos principales y de error están cubiertos | ✅ | 19 pruebas pasan: caminos felices, transiciones válidas e inválidas, estados terminales, duplicados, datos inválidos y salida del reporte. |
| Documentación | README, evidencias y decisiones están actualizados | ✅ | README, `evidencias.md` y este checklist describen el estado final. |
| Git | Historial de commits claro y ordenado | ✅ | Los cambios están agrupados por etapa y los commits describen la intención de cada uno. |
| Datos | No se usan datos personales reales | ✅ | Los ejemplos usan nombres y legajos sintéticos. |
| Complejidad | El módulo es legible y de bajo acoplamiento | ✅ | `sistema.py` tiene 158 líneas y responsabilidades separadas. |

## Observaciones y correcciones aplicadas

| ID | Hallazgo | Acción | Commit |
|---|---|---|---|
| R1 | `cambiar_estado` imprimía `"Estado inexistente"` y devolvía `False` | Se reemplazó por `EstadoInvalidoError` y se validó el tipo en la entidad | `c48cc16` |
| R2 | Se aceptaban IDs duplicados y campos vacíos | Se agregaron `SolicitudDuplicadaError`, `DatosInvalidosError` y validaciones en `DatosNuevaSolicitud` | `df43f70` |
| R3 | Nombres pobres, `return True` sin significado y `print` de éxito en el servicio | Se renombraron variables, se agregaron tipos y se sacó la presentación del gestor | `62b3ab4` |
| R4 | Artefactos de Python y entregables sin ignorar | Se agregó `.gitignore` con `__pycache__/`, `*.pyc` y `pdf/` | `773590c` |
| R5 | `Solicitud.cambiar_prioridad` lanzaba `TypeError` y faltaban casos de prueba | Se reemplazó por `DatosInvalidosError` y se amplió la suite a 19 pruebas | `8bf0e88` |

## Criterios de aceptación

- [x] El proyecto compila y `main.py` termina con código 0.
- [x] La suite de pruebas pasa completa.
- [x] No quedan errores silenciosos ni retornos `-1`/`False` sin explicación.
- [x] Los datos inválidos y los IDs duplicados se rechazan.
- [x] README y documentación de `docs/` describen el código actual.