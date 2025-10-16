# evento.py
from datetime import datetime, date

class Evento:
    def __init__(self, nome, data, hora, local, capacidade, categoria, preco, checkin=False):
        self.__nome = nome
        self.__data = data
        self.__hora = hora
        self.__local = local
        self.__capacidade = capacidade
        self.__categoria = categoria
        self.__preco = preco
        self.__participantes = []  # agora armazena objetos de Usuario

    # -------------------- GETTERS --------------------
    def get_nome(self):
        return self.__nome

    def get_data(self):
        return self.__data.strftime('%d/%m/%Y')
    
    def get_hora(self):
        return self.__hora.strftime('%H:%M')

    def get_categoria(self):
        return self.__categoria

    def get_preco(self):
        return self.__preco

    def get_local(self):
        return self.__local

    def get_participantes(self):
        return self.__participantes

    def get_vagas_disponiveis(self):
        return self.__capacidade - len(self.__participantes)

    # -------------------- VALIDAÇÃO DE DATA --------------------
    @staticmethod
    def validar_data_futura(data_str, formato='%d/%m/%Y'):
        agora = datetime.now()
        # Permite aceitar "-" ou "/"
        data_str = data_str.replace("-", "/")
        try:
            data_evento = datetime.strptime(data_str, formato)
        except ValueError:
            raise ValueError(f"Formato de data inválido. Use: {formato}")
        if data_evento.date() < agora.date():
            raise ValueError("A data do evento não pode ser anterior à data atual.")
        return data_evento

    # -------------------- INSCRIÇÃO --------------------
    def inscrever(self, usuario):
        """Inscreve o usuário logado no evento."""
        if self.get_vagas_disponiveis() <= 0:
            return False, "Evento lotado!"

        if usuario.get_email() in [u.get_email() for u in self.__participantes]:
            return False, "Usuário já inscrito neste evento!"

        self.__participantes.append(usuario)
        return True, "Inscrição realizada com sucesso!"

    # -------------------- CANCELAMENTO --------------------
    def cancelar_inscricao(self, email):
        """Remove um participante pelo e-mail."""
        for u in self.__participantes:
            if u.get_email() == email:
                self.__participantes.remove(u)
                return True, "Inscrição cancelada com sucesso."
        return False, "Participante não encontrado."

    # -------------------- RECEITA --------------------
    def calcular_receita(self):
        """Calcula receita total: número de inscritos * preço."""
        return len(self.__participantes) * self.__preco
    
    # -------------------- CHECK-IN --------------------
    def is_checkin_disponivel(self):
        """Verifica se a data atual é a mesma data do evento."""
        hoje = date.today()
        # self.__data é um objeto datetime, então pegamos apenas a parte da data com .date()
        data_do_evento = self.__data.date()
        return hoje == data_do_evento

    # -------------------- DETALHES --------------------
    def detalhes(self):
        return (
            f"{'='*50}\n"
            f"🎟️  Detalhes do Evento\n"
            f"Nome: {self.get_nome()}\n"
            f"Data: {self.get_data()} {self.get_hora()}\n"
            f"Local: {self.get_local()}\n"
            f"Categoria: {self.get_categoria()}\n"
            f"Preço: R$ {self.get_preco():.2f}\n"
            f"Vagas disponíveis: {self.get_vagas_disponiveis()}\n"
            f"Participantes inscritos: {len(self.__participantes)}\n"
            f"{'='*50}\n"
        )
