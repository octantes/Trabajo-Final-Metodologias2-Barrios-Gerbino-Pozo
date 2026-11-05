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
class EstadoInvalidoError(Exception): pass
class DatosInvalidosError(Exception): pass
class SolicitudDuplicadaError(Exception): pass


@dataclass(frozen=True)
class DatosNuevaSolicitud:
    # se agrupan estos datos
    id: int
    estudiante: Estudiante
    tipo_tramite: str
    motivo: str
    prioridad: Prioridad = Prioridad.MEDIA

    def __post_init__(self):
        # Fail Fast: los datos invalidos no deben llegar al dominio
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id <= 0:
            raise DatosInvalidosError(f"ID invalido: {self.id!r}")
        if not isinstance(self.estudiante, Estudiante):
            raise DatosInvalidosError("El estudiante es obligatorio")
        self._validar_texto("nombre del estudiante", self.estudiante.nombre)
        self._validar_texto("legajo del estudiante", self.estudiante.legajo)
        self._validar_texto("tipo de tramite", self.tipo_tramite)
        self._validar_texto("motivo", self.motivo)
        if not isinstance(self.prioridad, Prioridad):
            raise DatosInvalidosError(f"Prioridad invalida: {self.prioridad!r}")

    @staticmethod
    def _validar_texto(campo: str, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(f"El campo {campo} no puede estar vacio")

# 2. Entidad de dominio
class Solicitud:
    def __init__(self, datos: DatosNuevaSolicitud):
        self.id = datos.id
        self.estudiante = datos.estudiante
        self.tipo = datos.tipo_tramite
        self.motivo = datos.motivo
        self.estado = EstadoSolicitud.PENDIENTE
        # se suma este dato
        self.prioridad = datos.prioridad
        self.responsable = ""

        # OCP: Mapa de transiciones permitidas
        self._transiciones_permitidas = {
            EstadoSolicitud.PENDIENTE: [EstadoSolicitud.EN_TRAMITE, EstadoSolicitud.RECHAZADO],
            EstadoSolicitud.EN_TRAMITE: [EstadoSolicitud.RESUELTO]
        }

    def cambiar_estado(self, nuevo_estado: EstadoSolicitud):
        if not isinstance(nuevo_estado, EstadoSolicitud):
            raise EstadoInvalidoError(f"Estado invalido: {nuevo_estado!r}")
        if nuevo_estado in self._transiciones_permitidas.get(self.estado, []):
            self.estado = nuevo_estado
        else:
            raise TransicionInvalidaError(f"Transicion no valida de {self.estado.name} a {nuevo_estado.name}")

    def cambiar_prioridad(self, nueva_prioridad: Prioridad):
        if not isinstance(nueva_prioridad, Prioridad):
            raise TypeError("La prioridad debe ser de tipo Prioridad")
        self.prioridad = nueva_prioridad


class RepositorioSolicitudes:
    # se ocupa de guardar y buscar
    def __init__(self):
        self._solicitudes = []

    def agregar(self, solicitud: Solicitud):
        if any(existente.id == solicitud.id for existente in self._solicitudes):
            raise SolicitudDuplicadaError(f"Ya existe una solicitud con ID {solicitud.id}")
        self._solicitudes.append(solicitud)

    def obtener_por_id(self, id_sol) -> Solicitud:
        for solicitud in self._solicitudes:
            if solicitud.id == id_sol:
                return solicitud
        raise SolicitudNoEncontradaError(f"No se encontro la solicitud ID {id_sol}")

    def listar(self):
        return tuple(self._solicitudes)


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
        self._repositorio = RepositorioSolicitudes()
    
    def registrar_solicitud(self, datos: DatosNuevaSolicitud):
        nueva_solicitud = Solicitud(datos)
        self._repositorio.agregar(nueva_solicitud)
        return True

    def obtener_solicitud(self, id_sol) -> Solicitud:
        return self._repositorio.obtener_por_id(id_sol)

    def listar_solicitudes(self):
        return self._repositorio.listar()

    def asignar_responsable(self, id_sol, responsable):
        solicitud = self.obtener_solicitud(id_sol)
        solicitud.responsable = responsable
        print("responsable asignado con exito")

    def cambiar_estado(self, id_sol, estado: EstadoSolicitud | str):
        solicitud = self.obtener_solicitud(id_sol)
        if isinstance(estado, str):
            try:
                nuevo_estado = EstadoSolicitud(estado)
            except ValueError as exc:
                raise EstadoInvalidoError(f"Estado inexistente: {estado}") from exc
        elif isinstance(estado, EstadoSolicitud):
            nuevo_estado = estado
        else:
            raise EstadoInvalidoError(f"Estado invalido: {estado!r}")
        solicitud.cambiar_estado(nuevo_estado)

    def cambiar_prioridad(self, id_sol, nueva_prioridad: Prioridad):
        solicitud = self.obtener_solicitud(id_sol)
        solicitud.cambiar_prioridad(nueva_prioridad)

    def generar_reporte(self):
        GeneradorReportes.imprimir_reporte(self.listar_solicitudes())
