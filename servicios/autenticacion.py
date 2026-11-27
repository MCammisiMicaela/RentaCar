'''
Se gestionan las validaciones de login y registro de usuarios
'''
from datetime import datetime, date
from servicios.gestion_usuarios import cargar_usuarios
from servicios.seguridad import verificar_contrasena

from servicios.validaciones import (
    es_letras, es_fecha_valida, es_celular_valido,
    es_usuario_valido, es_contraseña_valida, coinciden_contraseñas
)

def validar_login(usuario, contraseña):
    if not usuario and not contraseña:
        return False, "Debe completar el nombre de usuario y la contraseña.", None
    if not usuario:
        return False, "Debe completar el nombre de usuario.", None
    if not contraseña:
        return False, "Debe completar la contraseña.", None

    usuarios = cargar_usuarios()
    usuario_obj = next((u for u in usuarios if u.usuario == usuario), None)
    if usuario_obj is None:
        return False, "El usuario ingresado no existe.", None

    # Comprobar el estado de la cuenta.
    if usuario_obj.bloqueado:
        return False, "La cuenta está bloqueada. Contacte al administrador.", None

    # Verificar que el usuario tenga un rol válido.
    if usuario_obj.tipo not in ["admin", "cliente"]:
        return False, "El tipo de usuario no está definido.", None

    # Verificar la contraseña usando su hash.
    if not verificar_contrasena(contraseña, usuario_obj.contraseña):
        return False, "La contraseña es incorrecta.", None

    return True, None, usuario_obj

def validar_registro(datos, usuarios_existentes, modo="registro"):
    errores = []

    campos_obligatorios = ["nombre", "apellido", "fecha_nacimiento", "celular", "usuario"]
    if modo == "registro":
        campos_obligatorios += ["contraseña", "confirmar_contraseña"]
    for campo in campos_obligatorios:
        valor = datos.get(campo)

        if campo == "fecha_nacimiento":
            if not isinstance(valor, (date, datetime)):
                errores.append("La fecha de nacimiento es obligatoria y debe ser válida.")
        else:
            if not isinstance(valor, str) or not valor.strip():
                errores.append(f"El campo '{campo}' es obligatorio.")

    if not es_letras(datos["nombre"]):
        errores.append("El nombre solo debe contener letras.")

    if not es_letras(datos["apellido"]):
        errores.append("El apellido solo debe contener letras.")

    estado_fecha = es_fecha_valida(datos["fecha_nacimiento"])
    if estado_fecha == "formato_invalido":
        errores.append("La fecha ingresada no es válida.")
    elif estado_fecha == "menor_edad":
        errores.append("Debés tener al menos 18 años para registrarte.")
    elif estado_fecha == "fecha_futura":
        errores.append("La fecha de nacimiento no puede ser posterior a hoy.")

    if not es_celular_valido(datos["celular"]):
        errores.append("El celular solo debe contener números.")

    estado_usuario = es_usuario_valido(datos["usuario"], usuarios_existentes, modo)

    if estado_usuario == "corto":
        errores.append("El nombre de usuario debe tener al menos 4 caracteres.")
    elif estado_usuario == "formato_invalido":
        errores.append("El nombre de usuario no debe contener espacios ni símbolos.")
    elif estado_usuario == "repetido":
        errores.append("El nombre de usuario ya está registrado.")

    if modo == "registro":
        if not es_contraseña_valida(datos["contraseña"]):
            errores.append("La contraseña debe tener al menos 6 caracteres, incluir letras y números.")
        if not coinciden_contraseñas(datos["contraseña"], datos["confirmar_contraseña"]):
            errores.append("Las contraseñas no coinciden.")

    tipo = datos.get("tipo")
    if tipo not in ["cliente", "admin"]:
        errores.append("El tipo de usuario no es válido.")

    return (False, errores) if errores else (True, ["Cuenta creada correctamente."])
