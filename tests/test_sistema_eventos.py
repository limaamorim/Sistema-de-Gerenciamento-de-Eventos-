import sys, os
# Adiciona o diretório raiz do projeto ao caminho do Python, 
# permitindo importar módulos como "models" e "sistema"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================================
# Importações de bibliotecas padrão e módulos do projeto
# ============================================================
import unittest
import json
from datetime import datetime, timedelta
from unittest.mock import patch

# Importa classes principais da aplicação
from models.usuario import Usuario
from models.admin import Administrador
from models.evento import Evento
from models.palestra import Palestra
from models.workshop import Workshop
from sistema.sistema_eventos import SistemaEventos
from sistema.autenticador import Autenticador
from data.persistencia_json import PersistenciaJSON
from data.persistencia_usuarios import PersistenciaUsuarios


# ============================================================
# Classe principal de testes unitários
# ============================================================
class TestSistemaEventos(unittest.TestCase):

    # ------------------------------------------------------------
    # Configuração inicial executada antes de cada teste
    # ------------------------------------------------------------
    def setUp(self):
        """Prepara ambiente de testes (executado antes de cada teste)"""
        # Garante que o diretório 'data' exista
        os.makedirs("data", exist_ok=True)

        # Se quiser limpar arquivos a cada teste, descomente:
        # open("data/eventos.json", "w").close()
        # open("data/usuarios.json", "w").close()

        # Cria uma nova instância do sistema e limpa eventos carregados
        self.sistema = SistemaEventos()
        self.sistema.eventos = []

        # Cria dados base para os testes
        self.data_futura = (datetime.now() + timedelta(days=2))
        self.hora = datetime.strptime("15:00", "%H:%M")

        # Cria usuários de exemplo
        self.usuario1 = Usuario("João", "joao@email.com", "123", "user")
        self.usuario2 = Usuario("Maria", "maria@email.com", "123", "user")
        self.admin = Administrador("Admin", "admin@email.com", "123")


    # ============================================================
    #  TESTES DE VALIDAÇÃO DE DATA
    # ============================================================
    def test_validar_data_futura_valida(self):
        """Deve aceitar uma data futura válida"""
        data_valida = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        data = Evento.validar_data_futura(data_valida)
        self.assertIsInstance(data, datetime)

    def test_validar_data_futura_invalida(self):
        """Deve lançar erro para data passada"""
        data_passada = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        with self.assertRaises(ValueError):
            Evento.validar_data_futura(data_passada)


    # ============================================================
    #  TESTE DE PERSISTÊNCIA (GRAVAR EVENTOS E USUÁRIOS NO JSON)
    # ============================================================
    def test_persistencia_(self):
        """Cria eventos e usuários e verifica se foram salvos no JSON"""

        # Cadastra um usuário no arquivo usuarios.json
        auth = Autenticador()
        auth.cadastrar_usuario("Lucas", "lucas@email.com", "senha123")

        # Cria eventos com diferentes tipos (Evento, Palestra, Workshop)
        data_futura = (datetime.now() + timedelta(days=5))
        hora = datetime.strptime("14:30", "%H:%M")

        evento = Evento("Evento Real", data_futura, hora, "Sala X", 10, "Educação", 50)
        palestra = Palestra("Palestra AI", self.data_futura, self.hora, "Auditório", 50, "IA", 0, "Prof. Silva")
        workshop = Workshop("WS Python", self.data_futura, self.hora, "Sala 1", 20, "Programação", 100, "Notebook", "Instrutor XPTO")

        # Adiciona todos os eventos à lista e salva no arquivo JSON
        self.sistema.eventos.extend([evento, palestra, workshop])
        self.sistema.salvar()

        print("\n✅ Evento e usuário reais salvos em /data/")

        # Verifica se o arquivo JSON contém os nomes dos eventos
        with open("data/eventos.json", "r", encoding="utf-8") as f:
            conteudo = f.read()

        self.assertIn("Evento Real", conteudo)
        self.assertIn("Palestra AI", conteudo)
        self.assertIn("WS Python", conteudo)


    # ============================================================
    #  TESTES DE INSCRIÇÃO E CANCELAMENTO
    # ============================================================
    def test_inscricao_sucesso(self):
        """Usuário deve conseguir se inscrever em um evento"""
        evento = Evento("Teste Evento", self.data_futura, self.hora, "Online", 2, "Tech", 50.0)
        sucesso, msg = evento.inscrever(self.usuario1)
        self.assertTrue(sucesso)
        self.assertIn("sucesso", msg.lower())

    def test_evento_lotado(self):
        """Deve impedir inscrição quando evento estiver cheio"""
        evento = Evento("Lotado", self.data_futura, self.hora, "Local", 1, "Tech", 10)
        evento.inscrever(self.usuario1)
        sucesso, msg = evento.inscrever(self.usuario2)
        self.assertFalse(sucesso)
        self.assertIn("lotado", msg.lower())

    def test_cancelar_inscricao(self):
        """Participante deve poder cancelar inscrição"""
        evento = Evento("Teste", self.data_futura, self.hora, "Online", 5, "Tech", 10)
        evento.inscrever(self.usuario1)
        sucesso, msg = evento.cancelar_inscricao(self.usuario1.get_email())
        self.assertTrue(sucesso)

    def test_cancelar_inscricao_inexistente(self):
        """Não deve cancelar se participante não estiver inscrito"""
        evento = Evento("Teste", self.data_futura, self.hora, "Online", 5, "Tech", 10)
        sucesso, msg = evento.cancelar_inscricao("naoexiste@email.com")
        self.assertFalse(sucesso)


    # ============================================================
    #  TESTES DE RECEITA E CHECK-IN
    # ============================================================
    def test_calcular_receita(self):
        """Deve calcular receita total com base nas inscrições"""
        evento = Evento("Evento Pago", self.data_futura, self.hora, "Local", 2, "Tech", 50)
        evento.inscrever(self.usuario1)
        evento.inscrever(self.usuario2)
        self.assertEqual(evento.calcular_receita(), 100)

    def test_checkin_disponivel_hoje(self):
        """Check-in deve estar disponível apenas no dia do evento"""
        hoje = datetime.now()
        evento_hoje = Evento("Hoje", hoje, hoje, "Local", 10, "Tech", 0)
        self.assertTrue(evento_hoje.is_checkin_disponivel())


    # ============================================================
    #  TESTE DE EXCLUSÃO DE EVENTOS (ADMIN)
    # ============================================================
    def test_deletar_evento_apenas_admin(self):
        """Apenas administradores podem excluir eventos"""
        evento = Evento("Apagar", self.data_futura, self.hora, "Local", 5, "Tech", 10)
        self.sistema.eventos.append(evento)

        # Simula entrada de confirmação "s" (mock do input)
        with patch("builtins.input", return_value="s"):
            self.sistema.deletar_evento(1, self.admin)

        # Após exclusão, lista de eventos deve estar vazia
        self.assertEqual(len(self.sistema.eventos), 0)


    # ============================================================
    #  TESTES DE AUTENTICAÇÃO E PERSISTÊNCIA DE USUÁRIOS
    # ============================================================
    def test_cadastrar_usuario_salva_no_json(self):
        """Cadastra usuário e verifica se foi salvo em usuarios.json"""
        auth = Autenticador()
        auth.cadastrar_usuario("Teste", "teste@email.com", "1234")

        with open("data/usuarios.json", "r", encoding="utf-8") as f:
            conteudo = f.read()

        self.assertIn("teste@email.com", conteudo)

    def test_login_sucesso(self):
        """Usuário deve conseguir fazer login com credenciais válidas"""
        auth = Autenticador()
        auth.cadastrar_usuario("User", "user@email.com", "123")
        usuario = auth.fazer_login("user@email.com", "123")
        self.assertIsNotNone(usuario)


# ============================================================
# Executa todos os testes quando o arquivo é rodado diretamente
# ============================================================
if __name__ == "__main__":
    unittest.main()
