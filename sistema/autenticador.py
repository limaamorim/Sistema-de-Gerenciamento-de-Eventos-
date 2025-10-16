from data.persistencia_usuarios import PersistenciaUsuarios
from models.usuario import Usuario
from models.admin import Administrador
import os

class Autenticador:
    def __init__(self):
        self.usuarios = PersistenciaUsuarios.carregar()

        if not any(u.get_tipo() == "admin" for u in self.usuarios):
            print("⚙️ Criando administrador padrão: admin@evento.com / senha: 1234")
            admin_padrao = Administrador("Admin Master", "admin@evento.com", "1234")
            self.usuarios.append(admin_padrao)
            PersistenciaUsuarios.salvar(self.usuarios)

    def fazer_login(self, email, senha):
        for usuario in self.usuarios:
            if usuario.autenticar(email, senha):
                print(f"✅ Login realizado com sucesso! Bem-vindo, {usuario.get_nome()}!")
                return usuario
        print("❌ E-mail ou senha inválidos.")
        return None

    def cadastrar_usuario(self, nome, email, senha):
        if any(u.get_email() == email for u in self.usuarios):
            print("❌ Já existe um usuário com esse e-mail.")
            return False

        novo_usuario = Usuario(nome, email, senha, "user")
        self.usuarios.append(novo_usuario)
        PersistenciaUsuarios.salvar(self.usuarios)
        print("✅ Usuário cadastrado com sucesso!")
        return True
    @staticmethod
    def limpar_tela ():
        os.system('cls' if os.name == 'nt' else 'clear')
