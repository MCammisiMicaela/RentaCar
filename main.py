from config.precarga_admin import crear_admin_general
from interfaces.comunes.login import mostrar_login

def iniciar_aplicacion():
    # Asegura que el administrador general esté registrado
    crear_admin_general()
    # Lanza la interfaz gráfica de inicio de sesión
    mostrar_login()


if __name__ == "__main__":
    iniciar_aplicacion()