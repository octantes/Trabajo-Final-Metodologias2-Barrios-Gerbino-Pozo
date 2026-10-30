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
