class Usuario:
    def __init__(self, nome, email, senha, tipo, chekin=False):
        self._nome = nome
        self._email = email
        self._senha = senha
        self._tipo = tipo  # "admin" ou "user"

    def autenticar(self, email, senha):
        """Verifica se o login está correto"""
        return self._email == email and self._senha == senha

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def get_tipo(self):
        return self._tipo
    
    def chekin(self):
        self.chekin = True

    def to_dict(self):
        """Converte para dicionário (para salvar em JSON)"""
        return {
            "nome": self._nome,
            "email": self._email,
            "senha": self._senha,
            "tipo": self._tipo
        }

    @staticmethod
    def from_dict(dados):
        """Cria um objeto UsuarioSistema a partir de dicionário"""
        return Usuario(dados["nome"], dados["email"], dados["senha"], dados["tipo"])
