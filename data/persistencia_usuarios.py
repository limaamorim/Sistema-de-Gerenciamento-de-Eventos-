import json
import os
from models.usuario import Usuario
from models.admin import Administrador

ARQUIVO_USUARIOS = "data/usuarios.json"
os.makedirs(os.path.dirname(ARQUIVO_USUARIOS), exist_ok=True)

class PersistenciaUsuarios:
    @staticmethod
    def salvar(usuarios):
        """Salva a lista de usuários no arquivo JSON."""
        dados = [u.to_dict() for u in usuarios]
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar():
        """Carrega os usuários do arquivo JSON."""
        if not os.path.exists(ARQUIVO_USUARIOS):
            return []

        # ⚙️ NOVO TRATAMENTO: se o arquivo estiver vazio, retorna lista vazia
        if os.path.getsize(ARQUIVO_USUARIOS) == 0:
            return []

        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                return []

        usuarios = []
        for d in dados:
            if d.get("tipo") == "admin":
                usuarios.append(Administrador(d["nome"], d["email"], d["senha"]))
            else:
                usuarios.append(Usuario(d["nome"], d["email"], d["senha"], d.get("tipo", "user")))
        return usuarios
