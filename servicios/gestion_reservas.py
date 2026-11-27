"""Reglas de negocio para reservas y puntuaciones de vehículos."""
from datetime import date
from uuid import uuid4
from clases.reserva import Reserva
from servicios.persistencia import cargar_json, guardar_json

RUTA_RESERVAS = "datos/reservas.json"
ESTADOS_OCUPADOS = ("activa", "pendiente")


def normalizar_reservas(datos):
    """Adapta estructuras anteriores en memoria sin descartar campos originales."""
    if isinstance(datos, list):
        entradas = [(str(i), r) for i, r in enumerate(datos)]
    elif isinstance(datos, dict):
        entradas = list(datos.items())
    else:
        raise ValueError("El contenido de reservas.json debe ser una lista o diccionario.")
    normalizadas = []
    for identificador, registro in entradas:
        if not isinstance(registro, dict):
            raise ValueError("Se encontró una reserva con formato inválido.")
        r = dict(registro)
        r["id_reserva"] = str(r.get("id_reserva") or f"LEGACY-{identificador}")
        auto = r.get("auto", "")
        if isinstance(auto, dict):
            auto = auto.get("patente", "")
        r["patente"] = str(r.get("patente") or auto)
        r["desde"] = str(r.get("desde") or r.get("fecha_inicio") or "")
        r["hasta"] = str(r.get("hasta") or r.get("fecha_fin") or "")
        r["estado"] = r.get("estado", "activa")
        r["puntaje"] = r.get("puntaje")
        normalizadas.append(r)
    return normalizadas


def actualizar_estado_reservas(reservas):
    reservas = normalizar_reservas(reservas)
    hoy = date.today()
    for reserva in reservas:
        if reserva.get("estado") == "activa":
            try:
                hasta = date.fromisoformat(reserva["hasta"])
            except (ValueError, TypeError):
                continue
            if hasta < hoy:
                reserva["estado"] = "finalizada"
    return reservas


def cargar_reservas(actualizar=True):
    reservas = cargar_json(RUTA_RESERVAS)
    if actualizar:
        actualizadas = actualizar_estado_reservas(reservas)
        if actualizadas != reservas:
            guardar_json(RUTA_RESERVAS, actualizadas)
        return actualizadas
    return reservas


def auto_disponible(patente, desde, hasta, reservas):
    try:
        d, h = date.fromisoformat(str(desde)), date.fromisoformat(str(hasta))
    except (ValueError, TypeError):
        return False
    if d > h:
        return False
    for reserva in normalizar_reservas(reservas):
        if str(reserva.get("patente", "")).strip().upper() != str(patente).strip().upper():
            continue
        if reserva.get("estado") not in ESTADOS_OCUPADOS:
            continue
        try:
            r_d = date.fromisoformat(reserva["desde"])
            r_h = date.fromisoformat(reserva["hasta"])
        except (ValueError, TypeError):
            # Una reserva activa incompleta no se descarta silenciosamente.
            return False
        if d <= r_h and h >= r_d:
            return False
    return True


def crear_reserva(usuario, patente, desde, hasta):
    from servicios.gestion_autos import cargar_autos
    try:
        d, h = date.fromisoformat(str(desde)), date.fromisoformat(str(hasta))
    except (ValueError, TypeError):
        return False, "Las fechas de la reserva no son válidas."
    if d < date.today() or h < d:
        return False, "El rango de fechas no es válido."
    auto = next((a for a in cargar_autos() if a.patente.upper() == patente.upper()), None)
    if auto is None:
        return False, "El vehículo no está registrado."
    if not auto.esta_disponible(d, h):
        return False, "El auto está bloqueado en ese período."
    reservas = cargar_reservas()
    if not auto_disponible(auto.patente, str(d), str(h), reservas):
        return False, "El auto no está disponible en ese período."
    numeros = []
    for r in reservas:
        rid = str(r.get("id_reserva", ""))
        if rid.startswith("R-") and rid[2:].isdigit():
            numeros.append(int(rid[2:]))
    nueva = Reserva(f"R-{max(numeros, default=0) + 1:04d}", auto.patente, usuario, str(d), str(h))
    reservas.append(nueva.to_dict())
    guardar_json(RUTA_RESERVAS, reservas)
    return True, "Reserva creada correctamente."


def cancelar_reserva(id_reserva, usuario=None):
    reservas = cargar_reservas()
    for r in reservas:
        if r.get("id_reserva") != id_reserva:
            continue
        if usuario is not None and r.get("usuario") != usuario:
            return False, "No tenés permisos para cancelar esta reserva."
        if r.get("estado") != "activa":
            return False, "Solo se pueden cancelar reservas activas."
        r["estado"] = "cancelada"
        guardar_json(RUTA_RESERVAS, reservas)
        return True, "Reserva cancelada correctamente."
    return False, "Reserva no encontrada."


def obtener_reservas_usuario(usuario):
    return [r for r in cargar_reservas() if r.get("usuario") == usuario]


def calificar_reserva(id_reserva, puntaje, usuario=None):
    if type(puntaje) is not int or not 1 <= puntaje <= 5:
        return False, "El puntaje debe estar entre 1 y 5."
    reservas = cargar_reservas()
    for r in reservas:
        if r.get("id_reserva") != id_reserva:
            continue
        if usuario is not None and r.get("usuario") != usuario:
            return False, "No tenés permisos para calificar esta reserva."
        if r.get("estado") != "finalizada":
            return False, "Solo se puede calificar una reserva finalizada."
        if r.get("puntaje") is not None:
            return False, "Esta reserva ya tiene una calificación."
        r["puntaje"] = puntaje
        guardar_json(RUTA_RESERVAS, reservas)
        return True, "¡Gracias por tu opinión!"
    return False, "Reserva no encontrada."
