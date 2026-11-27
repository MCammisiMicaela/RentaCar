from servicios.persistencia import cargar_json, guardar_json
from clases.auto import Auto
import os
from datetime import datetime, timedelta

RUTA_AUTOS = os.path.join("datos", "autos.json")

# Carga todos los autos desde el archivo JSON
def cargar_autos():
    datos = cargar_json(RUTA_AUTOS)
    if isinstance(datos, dict):
        registros = datos.values()
    elif isinstance(datos, list):
        registros = datos
    else:
        raise ValueError("El archivo autos.json tiene un formato inválido.")
    return [Auto.from_dict(auto_data) for auto_data in registros]

# Guarda la lista de autos en el archivo JSON
def guardar_autos(autos):
    datos = {auto.patente: auto.to_dict() for auto in autos}
    guardar_json(RUTA_AUTOS, datos)

# Busca un auto por su patente
def buscar_auto_por_patente(patente, autos):
    for auto in autos:
        if auto.patente == patente:
            return auto
    return None

# Agrega un nuevo auto a la lista y guarda
def agregar_auto(auto, autos):
    autos.append(auto)
    guardar_autos(autos)

# Modifica los datos de un auto existente y guarda
def modificar_auto(auto_modificado, autos):
    for i, auto in enumerate(autos):
        if auto.patente == auto_modificado.patente:
            autos[i] = auto_modificado
            break
    guardar_autos(autos)

from datetime import datetime
from servicios.persistencia import cargar_json, guardar_json

RUTA_AUTOS = "datos/autos.json"

def liberar_fechas_auto(patente, desde, hasta, accion="liberar"):
    """
    Gestiona las fechas de disponibilidad de un auto.

    accion puede ser:
        - "liberar": elimina las fechas de bloqueo dentro del rango
        - "bloquear": agrega el rango como no disponible
    """
    autos = cargar_json(RUTA_AUTOS)
    if patente not in autos:
        return

    auto = autos[patente]
    desde = datetime.strptime(desde, "%Y-%m-%d").date()
    hasta = datetime.strptime(hasta, "%Y-%m-%d").date()

    disponibilidad = auto.get("disponibilidad", [])

    if accion == "liberar":
        # Filtramos los rangos que NO se solapan con el rango liberado
        nueva_disp = []
        for rango in disponibilidad:
            d = datetime.strptime(rango["desde"], "%Y-%m-%d").date()
            h = datetime.strptime(rango["hasta"], "%Y-%m-%d").date()
            # Si el rango no se cruza con el que queremos liberar, lo mantenemos
            if h < desde or d > hasta:
                nueva_disp.append(rango)
        auto["disponibilidad"] = nueva_disp

    elif accion == "bloquear":
        # Agregamos el nuevo rango si no existe
        nuevo_rango = {"desde": desde.strftime("%Y-%m-%d"), "hasta": hasta.strftime("%Y-%m-%d")}
        # Evitamos duplicados o solapamientos
        if not any(
            datetime.strptime(r["desde"], "%Y-%m-%d").date() <= hasta and
            datetime.strptime(r["hasta"], "%Y-%m-%d").date() >= desde
            for r in disponibilidad
        ):
            disponibilidad.append(nuevo_rango)
        auto["disponibilidad"] = disponibilidad

    autos[patente] = auto
    guardar_json(RUTA_AUTOS, autos)
