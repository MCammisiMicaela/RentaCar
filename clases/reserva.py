class Reserva:
    def __init__(self, id_reserva, patente, usuario, desde, hasta, estado="activa", puntaje=None):
        # Inicializa los datos de la reserva
        self.id_reserva = id_reserva
        self.patente = patente
        self.usuario = usuario  # nombre de usuario
        self.desde = desde
        self.hasta = hasta
        self.estado = estado  # activa / finalizada / cancelada
        self.puntaje = puntaje  # int (1 a 5)

    def agregar_calificacion(self, puntaje):
        # Solo permite calificar si la reserva está finalizada
        if self.estado != "finalizada":
            raise ValueError("Solo se puede calificar una reserva finalizada.")
        self.puntaje = puntaje

    def to_dict(self):
        # Convierte la reserva a diccionario para guardar en JSON
        return {
            "id_reserva": self.id_reserva,
            "patente": self.patente,
            "usuario": self.usuario,
            "desde": self.desde,
            "hasta": self.hasta,
            "estado": self.estado,
            "puntaje": self.puntaje
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            id_reserva=datos["id_reserva"],
            patente=datos["patente"],
            usuario=datos["usuario"],
            desde=datos["desde"],
            hasta=datos["hasta"],
            estado=datos.get("estado", "activa"),
            puntaje=datos.get("puntaje")
        )
