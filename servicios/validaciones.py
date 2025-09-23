'''
Validaciones básicas por campo
'''
import re
from datetime import datetime, date


def es_letras(texto):
    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+", texto.strip()))

def es_fecha_valida(fecha):
    if isinstance(fecha, str):
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
        except ValueError:
            return "formato_invalido"

    if not isinstance(fecha, (date, datetime)):
        return "formato_invalido"

    hoy = date.today()
    if isinstance(fecha, datetime):
        fecha = fecha.date()

    edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))

    if edad < 18:
        return "menor_edad"

    if fecha > hoy:
        return "fecha_futura"

    return "valida"

def es_celular_valido(celular):
     return celular.isdigit() and len(celular) >= 8

def es_usuario_valido(usuario, existentes, modo):
    if len(usuario) < 4:
        return "corto"
    if not usuario.isalnum():
        return "formato_invalido"
    if usuario in existentes and modo != "edicion":
        return "repetido"
    return "valido"

def es_contraseña_valida(contraseña):
    return (
        len(contraseña) >= 6 and
        any(c.isdigit() for c in contraseña) and
        any(c.isalpha() for c in contraseña)
    )

def coinciden_contraseñas(contraseña, confirmacion):
    return contraseña == confirmacion

def validar_cambio_contraseña(actual, nueva, confirmacion, contraseña_guardada):
    if not actual or not nueva or not confirmacion:
        return False, "Todos los campos son obligatorios para cambiar la contraseña."

    if actual != contraseña_guardada:
        return False, "La contraseña actual no es válida."

    if len(nueva) < 4:
        return False, "La nueva contraseña debe tener al menos 4 caracteres."

    if nueva != confirmacion:
        return False, "La confirmación no coincide."

    return True, "Contraseña válida."