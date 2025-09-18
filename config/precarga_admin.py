'''
Crea el archivo usuarios.json si no existe
- Agrega el usuario "admin_general" con permisos exclusivos
'''
import json
import os

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def crear_admin_general():
    # Si el archivo no existe, lo crea vacío
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w") as archivo:
            json.dump({}, archivo)

    # Carga los usuarios existentes
    with open(RUTA_USUARIOS, "r") as archivo:
        usuarios = json.load(archivo)

    # Si no existe el admin_general, lo crea con todos los campos
    if "admin_general" not in usuarios:
        usuarios["admin_general"] = {
            "nombre": "Administrador",
            "apellido": "General",
            "fecha_nacimiento": "03/08/2001",
            "celular": "3496540538",
            "usuario": "admin_general",
            "contraseña": "admin123",
            "tipo": "admin",
            "bloqueado": False
        }

        with open(RUTA_USUARIOS, "w") as archivo:
            json.dump(usuarios, archivo, indent=4)