"""Lectura y escritura local de JSON con formatos compatibles."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def cargar_json(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return {} if ruta.name == "autos.json" else []
    with ruta.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)  # Un JSON inválido no se reemplaza silenciosamente.
    if ruta.name == "reservas.json":
        from servicios.gestion_reservas import normalizar_reservas
        return normalizar_reservas(datos)
    return datos


def guardar_json(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with NamedTemporaryFile("w", encoding="utf-8", dir=ruta.parent,
                                prefix=".rentacar_", suffix=".tmp", delete=False) as archivo:
            temporal = Path(archivo.name)
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()
