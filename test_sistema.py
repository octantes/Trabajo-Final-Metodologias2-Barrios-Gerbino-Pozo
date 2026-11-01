import unittest
from sistema import GestorSolicitudes, EstadoSolicitud, SolicitudNoEncontradaError, TransicionInvalidaError

class TestGestorSolicitudes(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada test para tener un entorno limpio
        self.gestor = GestorSolicitudes()
        self.gestor.registrar_solicitud(1, "Ana Gomez", "12345", "Equivalencia", "Solicito equivalencia")

    def test_registro_exitoso(self):
        # Verifica que la solicitud se haya guardado y tenga estado PENDIENTE
        solicitud = self.gestor.solicitudes[0]
        self.assertEqual(solicitud.id, 1)
        self.assertEqual(solicitud.estado, EstadoSolicitud.PENDIENTE)

    def test_asignacion_responsable(self):
        # Verifica la asignación de responsable
        self.gestor.asignar_responsable(1, "Secretaria Academica")
        self.assertEqual(self.gestor.solicitudes[0].responsable, "Secretaria Academica")

    def test_transicion_estado_valida(self):
        # Verifica el camino feliz de cambio de estado
        self.gestor.cambiar_estado(1, "EN_TRAMITE")
        self.assertEqual(self.gestor.solicitudes[0].estado, EstadoSolicitud.EN_TRAMITE)

    def test_transicion_estado_invalida(self):
        # Verifica que el sistema aborte si se salta un estado (Fail Fast / OCP)
        with self.assertRaises(TransicionInvalidaError):
            # No se puede pasar de PENDIENTE a RESUELTO directamente
            self.gestor.solicitudes[0].cambiar_estado(EstadoSolicitud.RESUELTO)

    def test_buscar_id_inexistente(self):
        # Verifica que lanzar error al buscar ID falso funcione
        with self.assertRaises(SolicitudNoEncontradaError):
            self.gestor.asignar_responsable(99, "Admin")

if __name__ == "__main__":
    unittest.main()