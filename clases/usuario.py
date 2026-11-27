class Usuario:
    def __init__(self, usuario, nombre, apellido, fecha_nacimiento, celular, contraseña, tipo, bloqueado=False):
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento  # string o date
        self.celular = celular
        self.contraseña = contraseña
        self.tipo = tipo
        self.bloqueado = bloqueado

    def modificar_datos_personales(self, nombre, apellido, fecha_nacimiento, celular):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.celular = celular

    def cambiar_contraseña(self, nueva_contraseña):
        from servicios.seguridad import crear_hash_contrasena
        self.contraseña = crear_hash_contrasena(nueva_contraseña)

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "celular": self.celular,
            "contraseña": self.contraseña,
            "tipo": self.tipo,
            "bloqueado": self.bloqueado
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            usuario=datos["usuario"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            celular=datos["celular"],
            contraseña=datos["contraseña"],
            tipo=datos["tipo"],
            bloqueado=datos.get("bloqueado", False)
        )