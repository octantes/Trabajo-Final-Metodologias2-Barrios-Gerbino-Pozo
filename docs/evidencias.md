## Etapa 3: Diagnostico de Deuda Tecnica y Code Smells

Al analizar la version base del sistema, se identificaron 8 problemas tecnicos que elevan la deuda tecnica y dificultan su mantenibilidad:

1. God Class:
   * Ubicacion: sistema.py, clase GestorSolicitudes.
   * Evidencia: La clase concentra multiples responsabilidades: almacena los datos en memoria, procesa reglas de negocio y genera salidas por consola.
   * Impacto: Alta centralizacion que hace que la clase tenga multiples motivos para cambiar.
   * Riesgo: Alto. 
   * Prioridad: Alta.

2. Long Parameter List - Lista Larga de Parametros:
   * Ubicacion: sistema.py, metodo registrar_solicitud.
   * Evidencia: La funcion recibe 5 parametros sueltos en su firma.
   * Impacto: Las firmas de los metodos son fragiles ante nuevos requerimientos.
   * Riesgo: Medio. 
   * Prioridad: Media.

3. Primitive Obsession - Obsesion por Primitivos:
   * Ubicacion: sistema.py, metodo registrar_solicitud.
   * Evidencia: Las solicitudes se instancian y almacenan como diccionarios en crudo en lugar de utilizar objetos de dominio.
   * Impacto: Impide encapsular el comportamiento propio de una solicitud.
   * Riesgo: Alto. 
   * Prioridad: Alta.

4. Magic Strings - Cadenas Magicas:
   * Ubicacion: sistema.py, a lo largo de toda la clase.
   * Evidencia: Los estados estan hardcodeados como literales de texto, ej. "PENDIENTE", "EN_TRAMITE".
   * Impacto: Propenso a errores tipograficos y dificulta la refactorizacion.
   * Riesgo: Medio. 
   * Prioridad: Alta.

5. Silenciamiento de Errores e Inadecuado Manejo:
   * Ubicacion: sistema.py, metodos registrar_solicitud y asignar_responsable.
   * Evidencia: Bloque except Exception con un pass - silencio total - y retornos de -1 ante errores.
   * Impacto: El sistema falla de manera silenciosa, dificultando el debugging.
   * Riesgo: Critico. 
   * Prioridad: Alta.

6. Duplicated Code - Codigo Duplicado:
   * Ubicacion: sistema.py, metodos asignar_responsable y cambiar_estado.
   * Evidencia: El bucle de busqueda por ID se repite exactamente igual en ambos metodos.
   * Impacto: Modificar la logica de busqueda obliga a cambiar multiples lugares.
   * Riesgo: Medio. 
   * Prioridad: Media.

7. Estructuras de Control Rigidas - Violacion OCP:
   * Ubicacion: sistema.py, metodo cambiar_estado.
   * Evidencia: Se utilizan bloques if-elif anidados extensos para validar las transiciones.
   * Impacto: Agregar un nuevo estado obliga a modificar esta estructura central.
   * Riesgo: Alto. 
   * Prioridad: Alta.

8. Poor Naming - Mal Nombramiento:
   * Ubicacion: sistema.py.
   * Evidencia: Nombres de variables poco descriptivos como lista_sol, s o req.
   * Impacto: Afecta la legibilidad y comprension del codigo.
   * Riesgo: Bajo. 
   * Prioridad: Baja.


## Etapa 4: Decisiones de Diseño (SOLID y Clean Code)

Para mitigar la deuda técnica detectada, se definieron las siguientes directrices de reestructuración arquitectónica:

1. **Aplicación de SRP:**
   * Se desacopló `GestorSolicitudes`: la impresión por consola quedó en `GeneradorReportes` y el almacenamiento en `RepositorioSolicitudes`.
   * Se creó la entidad de dominio `Solicitud` para encapsular la estructura de los datos, eliminando la obsesión por primitivos.
2. **Aplicación de OCP:**
   * Se eliminaron las estructuras `if-elif` anidadas en las transiciones de estado.
   * Se delegó la validación de transiciones a la propia clase `Solicitud` mediante un mapeo de estados permitidos.
3. **Clean Code:**
   * Se implementaron los `Enum` `EstadoSolicitud` y `Prioridad` para reemplazar las cadenas de texto hardcodeadas.
   * Se renombraron variables (`lista_sol` -> `_solicitudes`, `req` -> `solicitud`, `id_sol` -> `id_solicitud`) para que reflejen el lenguaje del negocio.
4. **Manejo de Errores:**
   * Se eliminaron los retornos silenciosos, los `print` de error y el uso de `pass`.
   * Se implementaron excepciones personalizadas (`SolicitudNoEncontradaError`, `TransicionInvalidaError`, `EstadoInvalidoError`, `DatosInvalidosError`, `SolicitudDuplicadaError`) para abortar flujos inválidos inmediatamente.
5. **Alcance de LSP, ISP y DIP:**
   * **LSP:** no se introdujeron jerarquías de herencia; las entidades no dependen de subtipos, por lo que no hay contratos que puedan romperse por sustitución.
   * **ISP:** las responsabilidades se separaron en componentes pequeños (`RepositorioSolicitudes` para almacenamiento y `GeneradorReportes` para salida), evitando que el gestor dependa de operaciones que no usa.
   * **DIP:** la persistencia quedó detrás de `RepositorioSolicitudes`; `GestorSolicitudes` todavía instancia la implementación concreta, por lo que la inyección por constructor queda como mejora pendiente.

## Etapa 5: Refactoring Seguro Aplicado

Se aplicaron las siguientes técnicas de refactoring documentadas sobre `sistema.py` para erradicar la deuda técnica, conservando intacto el comportamiento externo:

1. **Extract Method:** La búsqueda por ID se encapsuló en `RepositorioSolicitudes.obtener_por_id()`, eliminando la duplicación en `asignar_responsable` y `cambiar_estado`. La validación de campos de texto se extrajo a `DatosNuevaSolicitud._validar_texto()`.
2. **Move Method / Reubicación de Responsabilidad:** La impresión del reporte se trasladó a `GeneradorReportes` y el almacenamiento a `RepositorioSolicitudes`, dejando a `GestorSolicitudes` como orquestador.
3. **Introduce Parameter Object:** Se creó `DatosNuevaSolicitud` para agrupar ID, estudiante, tipo de trámite, motivo y prioridad, reemplazando la lista larga de parámetros.
4. **Replace Dictionary with Object:** Se creó la entidad `Solicitud` y el objeto de valor `Estudiante`, eliminando los diccionarios crudos y la obsesión por primitivos.
5. **Replace Magic Literal with Constant:** Se implementaron los enums `EstadoSolicitud` y `Prioridad`, y el mapa `_transiciones_permitidas` dentro de `Solicitud` reemplazó los `if-elif` anidados.
6. **Replace Error Code with Exception:** Se reemplazaron los retornos `-1`, los `print` y los `pass` por excepciones de dominio: `SolicitudNoEncontradaError`, `TransicionInvalidaError`, `EstadoInvalidoError`, `DatosInvalidosError` y `SolicitudDuplicadaError`.

*(Las capturas del "Antes y Después" se encuentran detalladas en el Informe PDF)*.

## Etapa 6: Pruebas y Verificación del Comportamiento

Para garantizar la estabilidad funcional y comprobar que las modificaciones de la Etapa 5 fueron seguras, se desarrolló una suite de pruebas unitarias utilizando `unittest`.

Se validaron los siguientes escenarios (19 pruebas):
- [x] **Camino Feliz:** Registro de solicitud con valores iniciales correctos.
- [x] **Flujo Operativo:** Asignación de responsable, cambio de prioridad y transición válida de estados (`PENDIENTE` a `EN_TRAMITE`).
- [x] **Protección de Dominio:** `SolicitudNoEncontradaError` ante IDs inexistentes.
- [x] **Reglas de Negocio (OCP):** `TransicionInvalidaError` al intentar `PENDIENTE` a `RESUELTO`.
- [x] **Estados inválidos:** `EstadoInvalidoError` ante un estado inexistente (`APROBADO`) o un string pasado directamente a la entidad.
- [x] **Aceptación del Enum:** `cambiar_estado` acepta `EstadoSolicitud` además de strings.
- [x] **Validación de datos:** `DatosInvalidosError` ante ID inválido y campos de texto vacíos (nombre, legajo, tipo y motivo).
- [x] **Duplicados:** `SolicitudDuplicadaError` al registrar un ID existente.
- [x] **Casos complementarios:** transiciones `PENDIENTE -> RECHAZADO` y `EN_TRAMITE -> RESUELTO`, bloqueo de estados terminales, IDs inexistentes en `cambiar_estado`/`cambiar_prioridad`, prioridad inválida y salida del reporte.

Ejecución:

```text
$ python3 -m unittest -v
Ran 19 tests in 0.001s
OK
```

### Antes / Después

| Escenario | Versión base (`a9786ab`) | Versión refactorizada |
|---|---|---|
| ID inexistente | `return -1` o `False` silencioso | `SolicitudNoEncontradaError` |
| Transición inválida | `print("transicion no valida")` | `TransicionInvalidaError` |
| Estado inexistente | Se aceptaba o fallaba sin control | `EstadoInvalidoError` |
| Datos vacíos | Se guardaban sin validar | `DatosInvalidosError` |
| ID duplicado | Se guardaba dos veces | `SolicitudDuplicadaError` |

La ejecución exitosa de la suite confirma que la calidad interna mejoró sin alterar negativamente el comportamiento externo esperado.