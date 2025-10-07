from datetime import datetime
from models.evento import Evento
from models.palestra import Palestra
from models.workshop import Workshop
from models.participante import Participante
from data.persistencia_json import PersistenciaJSON

class SistemaEventos:
    def __init__(self):
        self.eventos = PersistenciaJSON.carregar()

    def salvar(self):
        PersistenciaJSON.salvar(self.eventos)

    # ============================================================
    def cadastrar_evento(self, nome, data_str, local, capacidade, categoria, preco, tipo, extra=None):
        try:
            data = Evento.validar_data_futura(data_str)
        except ValueError as e:
            print(f"❌ Erro: {e}")
            return

        if capacidade <= 0 or preco < 0:
            print("⚠️ Capacidade e preço devem ser valores positivos.")
            return

        if tipo.lower() == "workshop":
            evento = Workshop(nome, data, local, capacidade, categoria, preco, extra)
        elif tipo.lower() == "palestra":
            evento = Palestra(nome, data, local, capacidade, categoria, preco, extra)
        else:
            evento = Evento(nome, data, local, capacidade, categoria, preco)

        self.eventos.append(evento)
        self.salvar()
        print("✅ Evento cadastrado com sucesso!")

    # ============================================================
    def listar_eventos(self):
        if not self.eventos:
            print("Nenhum evento cadastrado.")
            return
        for i, e in enumerate(self.eventos, start=1):
            print(f"\n[{i}] {e.detalhes()}")

    # ============================================================
    def buscar_por_categoria(self, categoria):
        if not categoria.strip():
            print("⚠️ Categoria não pode ser vazia.")
            return
        filtrados = [e for e in self.eventos if e.get_categoria().lower() == categoria.lower()]
        if not filtrados:
            print("Nenhum evento encontrado nessa categoria.")
            return
        for e in filtrados:
            print(f"\n{e.detalhes()}")

    # ============================================================
    def buscar_por_data(self, data_str):
        try:
            datetime.strptime(data_str, "%d-%m-%Y")
        except ValueError:
            print("❌ Data inválida. Use o formato dd-mm-YYYY.")
            return

        filtrados = [e for e in self.eventos if e.get_data().startswith(data_str[:5])]
        if not filtrados:
            print("Nenhum evento encontrado nessa data.")
            return
        for e in filtrados:
            print(f"\n{e.detalhes()}")

    # ============================================================
    def inscrever_participante(self, indice_evento, nome, email):
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print("❌ Evento inválido.")
            return

        if not nome or not email:
            print("⚠️ Nome e e-mail são obrigatórios.")
            return

        participante = Participante(nome, email)
        sucesso, msg = evento.inscrever(participante)
        print(msg)
        if sucesso:
            self.salvar()

    # ============================================================
    def cancelar_inscricao(self, indice_evento, email):
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print("❌ Evento inválido.")
            return

        sucesso, msg = evento.cancelar_inscricao(email)
        print(msg)
        if sucesso:
            self.salvar()

    # ============================================================
    def fazer_checkin(self, indice_evento, email):
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print("❌ Evento inválido.")
            return

        for p in evento.get_participantes():
            if p.get_email() == email:
                p.set_checkin()
                print("✅ Check-in realizado com sucesso!")
                self.salvar()
                return
        print("Participante não encontrado.")

    # ============================================================
    def relatorios(self):
        if not self.eventos:
            print("Nenhum evento cadastrado.")
            return
        print("\n--- Relatórios de Eventos ---")
        for e in self.eventos:
            print(f"\nEvento: {e.get_nome()}")
            print(f"Inscritos: {len(e.get_participantes())}")
            print(f"Vagas disponíveis: {e.get_vagas_disponiveis()}")
            print(f"Receita Total: R$ {e.calcular_receita():.2f}")
