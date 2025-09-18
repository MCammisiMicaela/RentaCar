'''
Se gestionan las validaciones de login y registro de usuarios
'''
import json
import os
from servicios.validaciones import (
    es_letras, es_fecha_valida, es_celular_valido,
    es_usuario_valido, es_contraseña_valida, coinciden_contraseñas
)

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def validar_login(usuario, contraseña):
    # Validación de campos vacíos
    if not usuario and not contraseña:
        return False, "Debe completar el nombre de usuario y la contraseña.", None
    if not usuario:
        return False, "Debe completar el nombre de usuario.", None
    if not contraseña:
        return False, "Debe completar la contraseña.", None

    # Cargar usuarios
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return False, "No se pudo acceder a los datos de usuarios.", None

    # Validación de existencia
    if usuario not in usuarios:
        return False, "El usuario ingresado no existe.",None

    datos = usuarios[usuario]

    # Validación de contraseña
    if datos["contraseña"] != contraseña:
        return False, "La contraseña es incorrecta.", None

    # Validación de bloqueo
    if datos["bloqueado"]:
        return False, "La cuenta está bloqueada. Contacte al administrador.", None

    # Éxito
    return True, f"Bienvenido {datos['nombre']} ({datos['tipo']})", datos["tipo"]

def validar_registro(datos, usuarios_existentes):
    errores = []
    
    campos_obligatorios = ["nombre", "apellido", "fecha_nacimiento", "celular", "usuario", "contraseña", "confirmar_contraseña"]
    for campo in campos_obligatorios:
        if not datos[campo].strip():
            errores.append(f"El campo '{campo}' es obligatorio.")

    if not es_letras(datos["nombre"]):
        errores.append("El nombre solo debe contener letras.")

    if not es_letras(datos["apellido"]):
        errores.append("El apellido solo debe contener letras.")

    estado_fecha = es_fecha_valida(datos["fecha_nacimiento"])
    if estado_fecha == "formato_invalido":
        errores.append("La fecha debe tener el formato DD/MM/AAAA.")
    elif estado_fecha == "menor_edad":
        errores.append("Debés tener al menos 18 años para registrarte.")
    elif estado_fecha == "fecha_futura":
        errores.append("La fecha de nacimiento no puede ser posterior a hoy.")

    if not es_celular_valido(datos["celular"]):
        errores.append("El celular solo debe contener números.")

    estado_usuario = es_usuario_valido(datos["usuario"], usuarios_existentes)

    if estado_usuario == "corto":
        errores.append("El nombre de usuario debe tener al menos 4 caracteres.")
    elif estado_usuario == "formato_invalido":
        errores.append("El nombre de usuario no debe contener espacios ni símbolos.")
    elif estado_usuario == "repetido":
        errores.append("El nombre de usuario ya está registrado.")

    if not es_contraseña_valida(datos["contraseña"]):
        errores.append("La contraseña debe tener al menos 6 caracteres, incluir letras y números.")

    if not coinciden_contraseñas(datos["contraseña"], datos["confirmar_contraseña"]):
        errores.append("Las contraseñas no coinciden.")

    if errores:
        return False, errores
    else:
        return True, ["Cuenta creada correctamente."]