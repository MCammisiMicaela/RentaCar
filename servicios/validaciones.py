'''
Validaciones básicas por campo
'''
import re
from datetime import datetime, date
import hmac
from servicios.seguridad import verificar_contrasena


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
    # Comprobar que todos los campos estén completos.
    if not actual or not nueva or not confirmacion:
        return False, "Todos los campos son obligatorios."

    # Comprobar la contraseña actual mediante su hash.
    if not verificar_contrasena(actual, contraseña_guardada):
        return False, "La contraseña actual no es válida."

    # Verificar los requisitos de la nueva contraseña.
    if not es_contraseña_valida(nueva):
        return False, (
            "La nueva contraseña debe tener al menos "
            "6 caracteres, incluir letras y números."
        )

    # Comprobar la confirmación.
    if nueva != confirmacion:
        return False, "La confirmación no coincide."

    return True, "Contraseña válida."
