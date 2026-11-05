from enum import Enum
from dataclasses import dataclass

# Reemplazo de magic strings por un enum
class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRAMITE = "EN_TRAMITE"
    RESUELTO = "RESUELTO"
    RECHAZADO = "RECHAZADO"


class Prioridad(Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


@dataclass(frozen=True)
class Estudiante:
    # se guarda aparte
    nombre: str
    legajo: str


# Excepciones personalizadas 
class SolicitudNoEncontradaError(Exception): pass
class TransicionInvalidaError(Exception): pass

# 2. Entidad de dominio
class Solicitud:
    def __init__(self, id_sol, estudiante, tipo_tramite, motivo):
        self.id = id_sol
        self.estudiante = estudiante
        self.tipo = tipo_tramite
        self.motivo = motivo
        self.estado = EstadoSolicitud.PENDIENTE
        # se suma este dato
        self.prioridad = Prioridad.MEDIA
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

    def cambiar_prioridad(self, nueva_prioridad: Prioridad):
        if not isinstance(nueva_prioridad, Prioridad):
            raise TypeError("La prioridad debe ser de tipo Prioridad")
        self.prioridad = nueva_prioridad

# 3. Delegación de responsabilidad SRP
class GeneradorReportes:
    @staticmethod
    def imprimir_reporte(solicitudes):
        print("\n--- REPORTE DE SOLICITUDES ---")
        for req in solicitudes:
            print(f"ID: {req.id} | Alumno: {req.estudiante.nombre} | Legajo: {req.estudiante.legajo} | Tramite: {req.tipo} | Prioridad: {req.prioridad.value} | Estado: {req.estado.value} | Resp: {req.responsable}")
        print("-----------------------------------------\n")

class GestorSolicitudes:
    def __init__(self):
        self.solicitudes = []
    
    def registrar_solicitud(self, id_sol, nombre_estudiante, legajo, tipo_tramite, motivo):
        estudiante = Estudiante(nombre_estudiante, legajo)
        nueva_solicitud = Solicitud(id_sol, estudiante, tipo_tramite, motivo)
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

    def cambiar_prioridad(self, id_sol, nueva_prioridad: Prioridad):
        solicitud = self._buscar_por_id(id_sol)
        solicitud.cambiar_prioridad(nueva_prioridad)

    def generar_reporte(self):
        GeneradorReportes.imprimir_reporte(self.solicitudes)
