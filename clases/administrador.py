from clases.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, usuario, nombre, apellido, fecha_nacimiento, celular, contraseña, tipo="admin", bloqueado=False):
        super().__init__(usuario, nombre, apellido, fecha_nacimiento, celular, contraseña, tipo, bloqueado)