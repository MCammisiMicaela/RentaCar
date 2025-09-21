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

def es_usuario_valido(usuario, existentes):
    if len(usuario) < 4:
        return "corto"
    if not usuario.isalnum():
        return "formato_invalido"
    if usuario in existentes:
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