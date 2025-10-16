from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha, "admin")
