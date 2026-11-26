
import hashlib
import hmac
import secrets

ITERACIONES = 600_000


def crear_hash_contrasena(contrasena):
    # Genera una sal aleatoria para cada contraseña.
    sal = secrets.token_bytes(16)

    # Deriva un hash seguro a partir de la contraseña.
    clave = hashlib.pbkdf2_hmac(
        "sha256",
        contrasena.encode("utf-8"),
        sal,
        ITERACIONES
    )

    # Guarda algoritmo, iteraciones, sal y hash.
    return f"pbkdf2_sha256${ITERACIONES}${sal.hex()}${clave.hex()}"


def verificar_contrasena(contrasena, valor_guardado):
    try:
        algoritmo, iteraciones, sal_hex, clave_hex = valor_guardado.split("$")

        if algoritmo != "pbkdf2_sha256":
            return False

        cantidad = int(iteraciones)
        if cantidad < 1 or cantidad > 1_000_000:
            return False

        sal = bytes.fromhex(sal_hex)
        clave_esperada = bytes.fromhex(clave_hex)

        clave_calculada = hashlib.pbkdf2_hmac(
            "sha256",
            contrasena.encode("utf-8"),
            sal,
            cantidad
        )

        return hmac.compare_digest(clave_calculada, clave_esperada)

    except (ValueError, AttributeError, TypeError):
        return False
