from datetime import datetime
from models.evento import Evento
from models.palestra import Palestra
from models.workshop import Workshop
from data.persistencia_json import PersistenciaJSON
from cores import Cores


class SistemaEventos:
    def __init__(self):
        self.eventos = PersistenciaJSON.carregar()

    def salvar(self):
        PersistenciaJSON.salvar(self.eventos)

    # ============================================================
    def cadastrar_evento(self, nome=None, data_str=None, hora=None, local=None,
                         capacidade=None, categoria=None, preco=None, tipo=None, extra=None):
        # ====== Nome ======
        while not nome:
            nome = input("Digite o nome do evento: ").strip()
            if not nome:
                print(f"{Cores.AMARELO}⚠️ O nome é obrigatório.{Cores.RESET}")

        # ====== Data ======
        while True:
            if not data_str:
                data_str = input("Digite a data do evento (DD/MM/AAAA ou DD-MM-AAAA): ").strip()

            # Permite usar / ou -
            data_str = data_str.replace("-", "/")

            try:
                data = Evento.validar_data_futura(data_str)
                break
            except ValueError as e:
                print(f"{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")
                data_str = None


        # ====== Hora ======
        while True:
            if not hora:
                hora = input("Digite o horário do evento (HH:MM): ").strip()
            try:
                hora_obj = datetime.strptime(hora, "%H:%M")
                break
            except ValueError:
                print(f"{Cores.VERMELHO}❌ Hora inválida. Use o formato HH:MM.{Cores.RESET}")
                hora = None

        # ====== Local ======
        while not local:
            local = input("Digite o local do evento: ").strip()
            if not local:
                print(f"{Cores.AMARELO}⚠️ O local é obrigatório.{Cores.RESET}")

        # ====== Capacidade ======
        while True:
            if capacidade is None:
                try:
                    capacidade = int(input("Digite a capacidade (número de pessoas): "))
                except ValueError:
                    print(f"{Cores.VERMELHO}❌ Digite um número válido.{Cores.RESET}")
                    continue
            if capacidade <= 0:
                print(f"{Cores.VERMELHO}⚠️ Capacidade deve ser positiva.{Cores.RESET}")
                capacidade = None
            else:
                break

        # ====== Categoria ======
        while not categoria:
            categoria = input("Digite a categoria do evento: ").strip()
            if not categoria:
                print(f"{Cores.AMARELO}⚠️ Categoria é obrigatória.{Cores.RESET}")

        # ====== Preço ======
        while True:
            if preco is None:
                try:
                    preco = float(input("Digite o preço do ingresso (R$): ").replace(',', '.'))
                except ValueError:
                    print(f"{Cores.VERMELHO}❌ Digite um valor numérico válido.{Cores.RESET}")
                    continue
            if preco < 0:
                print(f"{Cores.VERMELHO}⚠️ Preço não pode ser negativo.{Cores.RESET}")
                preco = None
            else:
                break

        # ====== Tipo ======
        while tipo not in ("1", "2", "3"):
            print("\nTipos disponíveis:")
            print("1 - Evento geral")
            print("2 - Palestra")
            print("3 - Workshop")
            tipo = input("Escolha o tipo do evento: ").strip()
            if tipo not in ("1", "2", "3"):
                print(f"{Cores.AMARELO}⚠️ Tipo inválido. Escolha 1, 2 ou 3.{Cores.RESET}")

        # ====== Extra ======
        if tipo == "2":
            while not extra:
                extra = input("Digite o nome do palestrante: ").strip()
                if not extra:
                    print(f"{Cores.AMARELO}⚠️ Nome do palestrante é obrigatório.{Cores.RESET}")
        elif tipo == "3":
            while not extra:
                extra = input("Digite o tema do workshop: ").strip()
                if not extra:
                    print(f"{Cores.AMARELO}⚠️ Tema do workshop é obrigatório.{Cores.RESET}")

        # ====== Criação do objeto ======
        if tipo == "3":
            evento = Workshop(nome, data, hora_obj, local, capacidade, categoria, preco, extra)
        elif tipo == "2":
            evento = Palestra(nome, data, hora_obj, local, capacidade, categoria, preco, extra)
        else:
            evento = Evento(nome, data, hora_obj, local, capacidade, categoria, preco)

        self.eventos.append(evento)
        self.salvar()
        print(f"{Cores.VERDE}✅ Evento cadastrado com sucesso!{Cores.RESET}")

    # ============================================================
    def listar_eventos(self):
        if not self.eventos:
            print(f"{Cores.AMARELO}⚠️ Nenhum evento cadastrado.{Cores.RESET}")
            return
        print(f"\n{Cores.ROXO}{'=' * 50}{Cores.RESET}")
        for i, e in enumerate(self.eventos, start=1):
            print(f"{Cores.CIANO}[{i}]{Cores.RESET} {e.get_nome()} - {e.get_data()} {e.get_hora()} | "
                  f"Categoria: {e.get_categoria()} | Vagas: {e.get_vagas_disponiveis()}")
        print(f"{Cores.ROXO}{'=' * 50}{Cores.RESET}")

    # ============================================================
    def inscrever_participante(self, indice_evento, usuario):
        """Agora inscreve o próprio usuário logado"""
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print(f"{Cores.VERMELHO}❌ Evento inválido.{Cores.RESET}")
            return

        sucesso, msg = evento.inscrever(usuario)
        print(f"{Cores.VERDE if sucesso else Cores.VERMELHO}{msg}{Cores.RESET}")
        if sucesso:
            self.salvar()

    # ============================================================
        # ============================================================
    def listar_categorias_enumeradas(self):
        """Lista todas as categorias únicas dos eventos"""
        if not self.eventos:
            print(f"{Cores.AMARELO}⚠️ Nenhum evento cadastrado.{Cores.RESET}")
            return []

        # Extrai categorias de objetos
        categorias = {e.get_categoria() for e in self.eventos if hasattr(e, "get_categoria")}
        categorias = sorted(categorias)  # ordena alfabeticamente

        if not categorias:
            print("⚠️ Nenhuma categoria cadastrada.")
            return []

        print("\n=== Categorias disponíveis ===")
        for i, cat in enumerate(categorias, start=1):
            print(f"{i} - {cat}")

        return categorias

   
    # ============================================================

    def buscar_por_categoria(self, categoria):
        """Filtra e mostra eventos de uma categoria específica"""
        eventos_filtrados = [
            e for e in self.eventos
            if hasattr(e, "get_categoria") and e.get_categoria().lower() == categoria.lower()
        ]

        if not eventos_filtrados:
            print(f"{Cores.AMARELO}⚠️ Nenhum evento encontrado na categoria '{categoria}'.{Cores.RESET}")
            return

        print(f"\n{Cores.NEGRITO}{Cores.ROXO}📚 Eventos da categoria: {categoria}{Cores.RESET}")
        for i, e in enumerate(eventos_filtrados, start=1):
            print(f"{Cores.CIANO}[{i}]{Cores.RESET} {e.get_nome()} - {e.get_data()} às {e.get_hora()} | "
                  f"Local: {e.get_local()} | Vagas: {e.get_vagas_disponiveis()}")

    # ============================================================

    def buscar_por_data(self, data_inicial=None, data_final=None):
        """Permite buscar eventos em uma data ou intervalo de datas"""
        from datetime import datetime

        formato = "%d/%m/%Y"  # Mantém o mesmo formato usado no cadastro

        # Pede intervalo se não for passado
        if not data_inicial:
            data_inicial = input("Data inicial (dd/mm/YYYY): ").strip()
        if not data_final:
            data_final = input("Data final (dd/mm/YYYY): ").strip()

        try:
            # Permite que o usuário digite com / ou -
            data_inicial = data_inicial.replace("-", "/")
            data_final = data_final.replace("-", "/")

            inicio = datetime.strptime(data_inicial, formato)
            fim = datetime.strptime(data_final, formato)
        except ValueError:
            print(f"{Cores.VERMELHO}❌ Formato de data inválido. Use dd/mm/YYYY ou dd-mm-YYYY.{Cores.RESET}")
            return

        if fim < inicio:
            print(f"{Cores.VERMELHO}⚠️ A data final não pode ser anterior à inicial.{Cores.RESET}")
            return

        eventos_filtrados = [
            e for e in self.eventos
            if hasattr(e, "get_data")
            and inicio <= datetime.strptime(e.get_data(), formato) <= fim
        ]

        if not eventos_filtrados:
            print(f"{Cores.AMARELO}⚠️ Nenhum evento encontrado no período informado.{Cores.RESET}")
            return

        print(f"\n{Cores.NEGRITO}{Cores.ROXO}📅 Eventos de {data_inicial} até {data_final}:{Cores.RESET}")
        for i, e in enumerate(eventos_filtrados, start=1):
            print(
                f"{Cores.CIANO}[{i}]{Cores.RESET} {e.get_nome()} - {e.get_data()} às {e.get_hora()} | "
                f"Categoria: {e.get_categoria()} | Local: {e.get_local()}"
            )

    # ============================================================
    def cancelar_inscricao(self, indice_evento, usuario):
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print(f"{Cores.VERMELHO}❌ Evento inválido.{Cores.RESET}")
            return

        sucesso, msg = evento.cancelar_inscricao(usuario.get_email())
        print(f"{Cores.VERDE if sucesso else Cores.VERMELHO}{msg}{Cores.RESET}")
        if sucesso:
            self.salvar()

    # ============================================================
        
    def listar_eventos_inscritos(self, usuario):
        """Mostra apenas os eventos em que o usuário está inscrito"""
        eventos_inscritos = [
            e for e in self.eventos
            if any(u.get_email() == usuario.get_email() for u in e.get_participantes())
        ]

        if not eventos_inscritos:
            print(f"{Cores.AMARELO}⚠️ Você não está inscrito em nenhum evento.{Cores.RESET}")
            return []

        print(f"\n{Cores.ROXO}{'=' * 50}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.AZUL}📋 Seus Eventos Inscritos:{Cores.RESET}")
        for i, e in enumerate(eventos_inscritos, start=1):
            print(f"{Cores.CIANO}[{i}]{Cores.RESET} {e.get_nome()} - {e.get_data()} às {e.get_hora()} | "
                  f"Local: {e.get_local()} | Categoria: {e.get_categoria()}")
        print(f"{Cores.ROXO}{'=' * 50}{Cores.RESET}")

        return eventos_inscritos
    
    # ============================================================
    def deletar_evento(self, indice_evento, usuario):
        """Permite que apenas o administrador exclua eventos"""
        try:
            evento = self.eventos[indice_evento - 1]
        except (IndexError, ValueError):
            print(f"{Cores.VERMELHO}❌ Evento inválido.{Cores.RESET}")
            return

        # Verifica se o usuário é admin
        if usuario.get_tipo() != "admin":
            print(f"{Cores.AMARELO}⚠️ Apenas administradores podem excluir eventos.{Cores.RESET}")
            return

        print(f"{Cores.AMARELO}⚠️ Você está prestes a excluir o evento: {Cores.RESET}{evento.get_nome()}")
        confirm = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
        if confirm == "s":
            self.eventos.remove(evento)
            self.salvar()
            print(f"{Cores.VERDE}✅ Evento excluído com sucesso!{Cores.RESET}")
        else:
            print(f"{Cores.AZUL}ℹ️ Exclusão cancelada.{Cores.RESET}")
            
    # ============================================================

    def relatorios(self):
        if not self.eventos:
            print(f"{Cores.AMARELO}⚠️ Nenhum evento cadastrado.{Cores.RESET}")
            return
        print(f"\n{Cores.NEGRITO}{Cores.ROXO}📊 Relatórios de Eventos{Cores.RESET}")
        for e in self.eventos:
            print(f"\n{Cores.AZUL}Evento:{Cores.RESET} {e.get_nome()}")
            print(f"Inscritos: {len(e.get_participantes())}")
            print(f"Vagas disponíveis: {e.get_vagas_disponiveis()}")
            print(f"Receita Total: R$ {e.calcular_receita():.2f}")
    
    # ============================================================

