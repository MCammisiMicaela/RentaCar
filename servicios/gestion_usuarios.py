import json
import os
from clases.usuario import Usuario
from clases.administrador import Administrador
from clases.cliente import Cliente

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def cargar_usuarios():
    usuarios = []
    if os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            for usuario_data in datos.values():
                tipo = usuario_data.get("tipo")
                if tipo == "admin":
                    usuario = Administrador.from_dict(usuario_data)
                elif tipo == "cliente":
                    usuario = Cliente.from_dict(usuario_data)
                else:
                    usuario = Usuario.from_dict(usuario_data)
                usuarios.append(usuario)
    return usuarios

def guardar_usuarios(usuarios):
    datos = {u.usuario: u.to_dict() for u in usuarios}
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

def buscar_usuario_por_nombre(usuario_nombre, usuarios):
    for usuario in usuarios:
        if usuario.usuario == usuario_nombre:
            return usuario
    return None

def agregar_usuario(usuario, usuarios):
    usuarios.append(usuario)
    guardar_usuarios(usuarios)

def modificar_usuario(usuario_modificado, usuarios):
    for i, usuario in enumerate(usuarios):
        if usuario.usuario == usuario_modificado.usuario:
            usuarios[i] = usuario_modificado
            break
    guardar_usuarios(usuarios)