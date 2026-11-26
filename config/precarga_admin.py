
import json
import os

from servicios.seguridad import crear_hash_contrasena
from servicios.validaciones import es_contraseña_valida

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")


def crear_admin_general():
    # Crear la carpeta de datos si todavía no existe.
    os.makedirs("datos", exist_ok=True)

    # Crear el archivo si todavía no existe.
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo)

    # Cargar los usuarios registrados.
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
        usuarios = json.load(archivo)

    # Si el administrador general ya existe, conservarlo.
    if "admin_general" in usuarios:
        return

    # Obtener la contraseña desde una variable de entorno.
    contraseña = os.environ.get("RENTACAR_ADMIN_PASSWORD")

    if not contraseña:
        raise RuntimeError(
            "Para crear el administrador inicial, configurá "
            "la variable RENTACAR_ADMIN_PASSWORD."
        )

    if len(contraseña) < 12 or not es_contraseña_valida(contraseña):
        raise ValueError(
            "La contraseña inicial debe tener al menos "
            "12 caracteres, incluyendo letras y números."
        )

    # Crear el administrador sin guardar la contraseña original.
    usuarios["admin_general"] = {
        "usuario": "admin_general",
        "nombre": "Administrador",
        "apellido": "General",
        "fecha_nacimiento": "01/01/2000",
        "celular": "",
        "contraseña": crear_hash_contrasena(contraseña),
        "tipo": "admin",
        "bloqueado": False
    }

    # Guardar el registro protegido.
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)
