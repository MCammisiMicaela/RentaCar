from datetime import date, datetime


class Auto:
    """Entidad de vehículo; la disponibilidad representa bloqueos manuales."""

    def __init__(self, patente, marca, modelo, categoria, transmision, pasajeros,
                 color, precio_por_dia, foto, bloqueado=False, disponibilidad=None,
                 datos_adicionales=None):
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.categoria = categoria
        self.transmision = transmision
        self.pasajeros = pasajeros
        self.color = color
        self.precio_por_dia = precio_por_dia
        self.foto = foto
        self.bloqueado = bloqueado
        self.disponibilidad = disponibilidad if isinstance(disponibilidad, list) else []
        self.datos_adicionales = dict(datos_adicionales or {})

    def esta_disponible(self, fecha_desde, fecha_hasta):
        if self.bloqueado:
            return False
        if isinstance(fecha_desde, str):
            fecha_desde = date.fromisoformat(fecha_desde)
        if isinstance(fecha_hasta, str):
            fecha_hasta = date.fromisoformat(fecha_hasta)
        for periodo in self.disponibilidad:
            try:
                desde = date.fromisoformat(periodo["desde"])
                hasta = date.fromisoformat(periodo["hasta"])
            except (TypeError, ValueError, KeyError):
                continue
            if fecha_desde <= hasta and fecha_hasta >= desde:
                return False
        return True

    def bloquear(self):
        self.bloqueado = True

    def desbloquear(self):
        self.bloqueado = False

    def to_dict(self):
        datos = dict(self.datos_adicionales)
        datos.update({
            "patente": self.patente, "marca": self.marca,
            "modelo": self.modelo, "categoria": self.categoria,
            "transmision": self.transmision, "pasajeros": self.pasajeros,
            "color": self.color, "precio_por_dia": self.precio_por_dia,
            "foto": self.foto, "bloqueado": self.bloqueado,
            "disponibilidad": self.disponibilidad,
        })
        return datos

    @classmethod
    def from_dict(cls, datos):
        # La versión anterior podía guardar "caracteristica" sin "transmision".
        transmision = datos.get("transmision")
        if not transmision:
            candidata = str(datos.get("caracteristica", "")).strip()
            transmision = candidata if candidata.lower() in ("manual", "automático", "automatico") else "Sin especificar"
        conocidos = {"patente", "marca", "modelo", "categoria", "transmision",
                     "pasajeros", "color", "precio_por_dia", "foto",
                     "bloqueado", "disponibilidad"}
        extras = {k: v for k, v in datos.items() if k not in conocidos}
        precio = datos.get("precio_por_dia", 0)
        try:
            precio = float(precio)
        except (ValueError, TypeError):
            precio = 0.0
        return cls(
            patente=datos.get("patente", ""), marca=datos.get("marca", ""),
            modelo=datos.get("modelo", ""), categoria=datos.get("categoria", ""),
            transmision=transmision, pasajeros=datos.get("pasajeros", 0),
            color=datos.get("color", ""), precio_por_dia=precio,
            foto=datos.get("foto", ""), bloqueado=datos.get("bloqueado", False),
            disponibilidad=datos.get("disponibilidad", []),
            datos_adicionales=extras,
        )
