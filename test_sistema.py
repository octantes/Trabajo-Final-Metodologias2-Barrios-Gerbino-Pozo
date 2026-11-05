import io
import unittest
from contextlib import redirect_stdout

from sistema import (
    DatosInvalidosError,
    DatosNuevaSolicitud,
    EstadoInvalidoError,
    EstadoSolicitud,
    Estudiante,
    GestorSolicitudes,
    Prioridad,
    SolicitudDuplicadaError,
    SolicitudNoEncontradaError,
    TransicionInvalidaError,
)

class TestGestorSolicitudes(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada test para tener un entorno limpio
        self.gestor = GestorSolicitudes()
        self.gestor.registrar_solicitud(
            DatosNuevaSolicitud(
                id=1,
                estudiante=Estudiante("Ana Gomez", "12345"),
                tipo_tramite="Equivalencia",
                motivo="Solicito equivalencia",
            )
        )

    def test_registro_exitoso(self):
        # Verifica que la solicitud se haya guardado y tenga estado PENDIENTE
        solicitud = self.gestor.obtener_solicitud(1)
        self.assertEqual(solicitud.id, 1)
        self.assertEqual(solicitud.estado, EstadoSolicitud.PENDIENTE)
        self.assertEqual(solicitud.estudiante.nombre, "Ana Gomez")
        self.assertEqual(solicitud.estudiante.legajo, "12345")

    def test_asignacion_responsable(self):
        # Verifica la asignación de responsable
        self.gestor.asignar_responsable(1, "Secretaria Academica")
        self.assertEqual(self.gestor.obtener_solicitud(1).responsable, "Secretaria Academica")

    def test_cambiar_prioridad(self):
        self.assertEqual(self.gestor.obtener_solicitud(1).prioridad, Prioridad.MEDIA)
        self.gestor.cambiar_prioridad(1, Prioridad.ALTA)
        self.assertEqual(self.gestor.obtener_solicitud(1).prioridad, Prioridad.ALTA)

    def test_transicion_estado_valida(self):
        # Verifica el camino feliz de cambio de estado
        self.gestor.cambiar_estado(1, "EN_TRAMITE")
        self.assertEqual(self.gestor.obtener_solicitud(1).estado, EstadoSolicitud.EN_TRAMITE)

    def test_transicion_estado_invalida(self):
        # Verifica que el sistema aborte si se salta un estado (Fail Fast / OCP)
        with self.assertRaises(TransicionInvalidaError):
            # No se puede pasar de PENDIENTE a RESUELTO directamente
            self.gestor.cambiar_estado(1, "RESUELTO")

    def test_estado_inexistente(self):
        # Un estado que no pertenece al Enum debe fallar de forma explicita
        with self.assertRaises(EstadoInvalidoError):
            self.gestor.cambiar_estado(1, "APROBADO")

    def test_transicion_estado_con_enum(self):
        # El gestor tambien debe aceptar el Enum directamente
        self.gestor.cambiar_estado(1, EstadoSolicitud.EN_TRAMITE)
        self.assertEqual(self.gestor.obtener_solicitud(1).estado, EstadoSolicitud.EN_TRAMITE)

    def test_solicitud_rechaza_estado_no_enum(self):
        # La entidad de dominio no debe aceptar strings sueltos
        with self.assertRaises(EstadoInvalidoError):
            self.gestor.obtener_solicitud(1).cambiar_estado("EN_TRAMITE")

    def test_buscar_id_inexistente(self):
        # Verifica que lanzar error al buscar ID falso funcione
        with self.assertRaises(SolicitudNoEncontradaError):
            self.gestor.asignar_responsable(99, "Admin")

    def test_registro_id_duplicado(self):
        # No deben existir dos solicitudes con el mismo ID
        datos = DatosNuevaSolicitud(
            id=1,
            estudiante=Estudiante("Otra Persona", "99999"),
            tipo_tramite="Certificado",
            motivo="Otro motivo",
        )
        with self.assertRaises(SolicitudDuplicadaError):
            self.gestor.registrar_solicitud(datos)
        self.assertEqual(len(self.gestor.listar_solicitudes()), 1)

    def test_registro_campos_vacios(self):
        # Los campos obligatorios no pueden quedar vacios
        with self.assertRaises(DatosInvalidosError):
            DatosNuevaSolicitud(
                id=2,
                estudiante=Estudiante("", "12345"),
                tipo_tramite="Equivalencia",
                motivo="Solicito equivalencia",
            )
        with self.assertRaises(DatosInvalidosError):
            DatosNuevaSolicitud(
                id=3,
                estudiante=Estudiante("Ana Gomez", "12345"),
                tipo_tramite="",
                motivo="Solicito equivalencia",
            )
        with self.assertRaises(DatosInvalidosError):
            DatosNuevaSolicitud(
                id=4,
                estudiante=Estudiante("Ana Gomez", "12345"),
                tipo_tramite="Equivalencia",
                motivo="   ",
            )

    def test_registro_id_invalido(self):
        # El ID debe ser un entero positivo
        with self.assertRaises(DatosInvalidosError):
            DatosNuevaSolicitud(
                id=0,
                estudiante=Estudiante("Ana Gomez", "12345"),
                tipo_tramite="Equivalencia",
                motivo="Solicito equivalencia",
            )

    def test_transicion_pendiente_a_rechazado(self):
        # PENDIENTE tambien puede pasar directamente a RECHAZADO
        self.gestor.cambiar_estado(1, "RECHAZADO")
        self.assertEqual(self.gestor.obtener_solicitud(1).estado, EstadoSolicitud.RECHAZADO)

    def test_transicion_en_tramite_a_resuelto(self):
        # El flujo completo del camino feliz debe llegar a RESUELTO
        self.gestor.cambiar_estado(1, "EN_TRAMITE")
        self.gestor.cambiar_estado(1, "RESUELTO")
        self.assertEqual(self.gestor.obtener_solicitud(1).estado, EstadoSolicitud.RESUELTO)

    def test_estado_terminal_no_permite_transicion(self):
        # Ni RESUELTO ni RECHAZADO deben volver a un estado anterior
        self.gestor.cambiar_estado(1, "EN_TRAMITE")
        self.gestor.cambiar_estado(1, "RESUELTO")
        with self.assertRaises(TransicionInvalidaError):
            self.gestor.cambiar_estado(1, "EN_TRAMITE")

        self.gestor.registrar_solicitud(
            DatosNuevaSolicitud(
                id=2,
                estudiante=Estudiante("Juan Perez", "98765"),
                tipo_tramite="Certificado",
                motivo="Certificado de alumno regular",
            )
        )
        self.gestor.cambiar_estado(2, "RECHAZADO")
        with self.assertRaises(TransicionInvalidaError):
            self.gestor.cambiar_estado(2, "EN_TRAMITE")

    def test_reporte_incluye_solicitudes(self):
        # El reporte debe mostrar los datos relevantes de cada solicitud
        salida = io.StringIO()
        with redirect_stdout(salida):
            self.gestor.generar_reporte()
        texto = salida.getvalue()
        self.assertIn("ID: 1", texto)
        self.assertIn("Alumno: Ana Gomez", texto)
        self.assertIn("Estado: PENDIENTE", texto)

    def test_cambiar_estado_id_inexistente(self):
        # Cambiar el estado de una solicitud inexistente debe fallar explicitamente
        with self.assertRaises(SolicitudNoEncontradaError):
            self.gestor.cambiar_estado(99, "EN_TRAMITE")

    def test_cambiar_prioridad_id_inexistente(self):
        # Cambiar la prioridad de una solicitud inexistente debe fallar explicitamente
        with self.assertRaises(SolicitudNoEncontradaError):
            self.gestor.cambiar_prioridad(99, Prioridad.ALTA)

    def test_prioridad_invalida(self):
        # La prioridad debe ser un valor del Enum, tanto al crear como al modificar
        with self.assertRaises(DatosInvalidosError):
            self.gestor.cambiar_prioridad(1, "ALTA")
        with self.assertRaises(DatosInvalidosError):
            DatosNuevaSolicitud(
                id=2,
                estudiante=Estudiante("Ana Gomez", "12345"),
                tipo_tramite="Equivalencia",
                motivo="Solicito equivalencia",
                prioridad="ALTA",
            )

if __name__ == "__main__":
    unittest.main()
