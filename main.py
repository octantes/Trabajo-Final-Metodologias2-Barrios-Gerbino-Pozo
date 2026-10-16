from sistema import GestorSolicitudes

if __name__ == "__main__":

    # 1 - instanciamos sistema
    gestor = GestorSolicitudes()

    # 2 - registramos solicitud nueva 
    gestor.registrar_solicitud(1, "Ana Gomez", "12345", "Equivalencia", "Solicito equivalencia de Matematica")
    gestor.registrar_solicitud(2, "Juan Perez", "98765", "Certificado", "Certificado de alumno regular")

    # 3 - asignamos responsables 
    gestor.asignar_responsable(1, "Secretaria Academica")
    
    # 4 - cambiamos estados
    gestor.cambiar_estado(1, "EN_TRAMITE")
    gestor.cambiar_estado(1, "RESUELTO")

    # 5 - generamos el reporte
    gestor.generar_reporte()
