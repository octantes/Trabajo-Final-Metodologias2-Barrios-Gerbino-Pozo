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
   * Desacoplar `GestorSolicitudes`. Se extraerá la impresión por consola a una nueva clase `GeneradorReportes`.
   * Crear la entidad de dominio `Solicitud` para encapsular la estructura de los datos, eliminando la obsesión por primitivos.
2. **Aplicación de OCP:**
   * Eliminar las estructuras `if-elif` anidadas en las transiciones de estado.
   * Delegar la validación de transiciones a la propia clase `Solicitud` mediante un mapeo de estados permitidos.
3. **Clean Code:**
   * Implementar `Enum` (`EstadoSolicitud`) para reemplazar las cadenas de texto hardcodeadas.
   * Renombrar variables (`lista_sol` -> `solicitudes`, `req` -> `solicitud`) para que reflejen el lenguaje del negocio.
4. **Manejo de Errores:**
   * Eliminar retornos silenciosos y el uso de `pass`.
   * Implementar excepciones personalizadas (`SolicitudNoEncontradaError`, `TransicionInvalidaError`) para abortar flujos inválidos inmediatamente.

## Etapa 5: Refactoring Seguro Aplicado

Se aplicaron 4 técnicas de refactoring documentadas sobre `sistema.py` para erradicar la deuda técnica, conservando intacto el comportamiento externo:

1. **Extract Method:** Se extrajo la lógica repetida de búsqueda de trámites hacia el método privado `_buscar_por_id()`, eliminando la duplicación en `asignar_responsable` y `cambiar_estado`.
2. **Move Method:** Se reubicó el método `generar_reporte()` desde la clase `GestorSolicitudes` hacia la nueva clase `GeneradorReportes`, cumpliendo con el principio SRP.
3. **Replace Dictionary with Object:** Se creó la clase `Solicitud` para instanciar objetos de dominio en `registrar_solicitud`, eliminando la obsesión por primitivos (diccionarios).
4. **Replace Magic Literal with Constant:** Se implementó el Enum `EstadoSolicitud` para tipar los estados, y un diccionario interno de `_transiciones_permitidas` que eliminó los múltiples `if-elif` anidados.

*(Las capturas del "Antes y Después" se encuentran detalladas en el Informe PDF)*.