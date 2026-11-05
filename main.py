from sistema import DatosNuevaSolicitud, Estudiante, GestorSolicitudes, Prioridad

if __name__ == "__main__":

    # 1 - instanciamos sistema
    gestor = GestorSolicitudes()

    # 2 - registramos solicitud nueva 
    gestor.registrar_solicitud(
        DatosNuevaSolicitud(
            id=1,
            estudiante=Estudiante("Ana Gomez", "12345"),
            tipo_tramite="Equivalencia",
            motivo="Solicito equivalencia de Matematica",
        )
    )
    gestor.registrar_solicitud(
        DatosNuevaSolicitud(
            id=2,
            estudiante=Estudiante("Juan Perez", "98765"),
            tipo_tramite="Certificado",
            motivo="Certificado de alumno regular",
        )
    )

    # 3 - asignamos responsables 
    gestor.asignar_responsable(1, "Secretaria Academica")
    gestor.cambiar_prioridad(2, Prioridad.ALTA)
    
    # 4 - cambiamos estados
    gestor.cambiar_estado(1, "EN_TRAMITE")
    gestor.cambiar_estado(1, "RESUELTO")

    # 5 - generamos el reporte
    gestor.generar_reporte()
