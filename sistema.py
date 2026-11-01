from enum import Enum

# Reemplazo de magic strings por un enum
class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRAMITE = "EN_TRAMITE"
    RESUELTO = "RESUELTO"
    RECHAZADO = "RECHAZADO"

# Excepciones personalizadas 
class SolicitudNoEncontradaError(Exception): pass
class TransicionInvalidaError(Exception): pass

# 2. Entidad de dominio
class Solicitud:
    def __init__(self, id_sol, nombre_estudiante, legajo, tipo_tramite, motivo):
        self.id = id_sol
        self.estudiante_nom = nombre_estudiante
        self.estudiante_leg = legajo
        self.tipo = tipo_tramite
        self.motivo = motivo
        self.estado = EstadoSolicitud.PENDIENTE
        self.responsable = ""

        # OCP: Mapa de transiciones permitidas
        self._transiciones_permitidas = {
            EstadoSolicitud.PENDIENTE: [EstadoSolicitud.EN_TRAMITE, EstadoSolicitud.RECHAZADO],
            EstadoSolicitud.EN_TRAMITE: [EstadoSolicitud.RESUELTO]
        }

    def cambiar_estado(self, nuevo_estado: EstadoSolicitud):
        if nuevo_estado in self._transiciones_permitidas.get(self.estado, []):
            self.estado = nuevo_estado
        else:
            raise TransicionInvalidaError(f"Transicion no valida de {self.estado.name} a {nuevo_estado.name}")

# 3. Delegación de responsabilidad SRP
class GeneradorReportes:
    @staticmethod
    def imprimir_reporte(solicitudes):
        print("\n--- REPORTE DE SOLICITUDES ---")
        for req in solicitudes:
            print(f"ID: {req.id} | Alumno: {req.estudiante_nom} | Tramite: {req.tipo} | Estado: {req.estado.value} | Resp: {req.responsable}")
        print("-----------------------------------------\n")

class GestorSolicitudes:
    def __init__(self):
        self.solicitudes = []
    
    def registrar_solicitud(self, id_sol, nombre_estudiante, legajo, tipo_tramite, motivo):
        # Ahora usamos la clase Solicitud en lugar de un diccionario
        nueva_solicitud = Solicitud(id_sol, nombre_estudiante, legajo, tipo_tramite, motivo)
        self.solicitudes.append(nueva_solicitud)
        return True

    # 4. Extract method 
    def _buscar_por_id(self, id_sol) -> Solicitud:
        for req in self.solicitudes:
            if req.id == id_sol:
                return req
        raise SolicitudNoEncontradaError(f"No se encontro la solicitud ID {id_sol}")

    def asignar_responsable(self, id_sol, responsable):
        solicitud = self._buscar_por_id(id_sol)
        solicitud.responsable = responsable
        print("responsable asignado con exito")

    def cambiar_estado(self, id_sol, estado_str):
        solicitud = self._buscar_por_id(id_sol)
        try:
            nuevo_estado = EstadoSolicitud(estado_str)
            solicitud.cambiar_estado(nuevo_estado)
            return True
        except ValueError:
            print("Estado inexistente")
            return False

    def generar_reporte(self):
        GeneradorReportes.imprimir_reporte(self.solicitudes)