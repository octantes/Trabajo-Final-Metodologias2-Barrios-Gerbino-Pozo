class GestorSolicitudes:
    """
    Sistema base con Large Class y violacion de SRP
    Esta clase hace de base de datos, valida, procesa logica de negocio e imprime reportes
    """
    def __init__(self):
        self.lista_sol = [] # mal nombre de variable
    
    # long parameter list (demasiados parametros)
    def registrar_solicitud(self, id_sol, nombre_estudiante, legajo, tipo_tramite, motivo):
        try:
            # obsesion por primitivos: todo se guarda en diccionario en lugar de objetos
            s = {
                "id": id_sol,
                "estudiante_nom": nombre_estudiante,
                "estudiante_leg": legajo,
                "tipo": tipo_tramite,
                "motivo": motivo,
                "estado": "PENDIENTE", # strings hardcodeados
                "responsable": ""
            }
            self.lista_sol.append(s)
            return True
        except Exception:
            # silencio de errores: catch vacío
            pass 

    def asignar_responsable(self, id_sol, responsable):
        # codigo duplicado: logica de buscar por id repetida en cada funcion
        encontrado = False
        for req in self.lista_sol:
            if req["id"] == id_sol:
                req["responsable"] = responsable
                encontrado = True
                print("responsable asignado con exito")
        
        # mal manejo de errores: retorna -1 en lugar de excepcion
        if not encontrado:
            return -1 

    # metodo largo y estructuras de control rigidas (violacion de OCP)
    def cambiar_estado(self, id_sol, nuevo_estado):
        for req in self.lista_sol:
            if req["id"] == id_sol:
                if req["estado"] == "PENDIENTE":
                    if nuevo_estado == "EN_TRAMITE" or nuevo_estado == "RECHAZADO":
                        req["estado"] = nuevo_estado
                    else:
                        print("transicion no valida")
                elif req["estado"] == "EN_TRAMITE":
                    if nuevo_estado == "RESUELTO":
                        req["estado"] = nuevo_estado
                    else:
                        print("transicion no valida")
                elif req["estado"] == "RESUELTO":
                    print("el tramite ya se encuentra cerrado")
                return True
        return False

    def generar_reporte(self):
        print("\n--- REPORTE DE SOLICITUDES ---")
        for req in self.lista_sol:
            print(f"ID: {req['id']} | Alumno: {req['estudiante_nom']} | Tramite: {req['tipo']} | Estado: {req['estado']} | Resp: {req['responsable']}")
        print("-----------------------------------------\n")
