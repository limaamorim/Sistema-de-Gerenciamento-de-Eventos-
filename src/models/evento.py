# evento.py
from datetime import datetime
from models.participante import Participante

class Evento:
    def __init__(self, nome, data, local, capacidade, categoria, preco):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__capacidade = int[capacidade] # Indicar que é valor numerico inteiro
        self.__categoria = categoria
        self.__preco = float(preco) #Indicar que é variavel numerica
        self.__participantes = []

    # Getters
    def get_nome(self):
        return self.__nome

    def get_data(self):
        return self.__data.strftime('%m-%d')

    def get_categoria(self):
        return self.__categoria

    def get_preco(self):
        return self.__preco

    def get_local(self):
        return self.__local

    def get_vagas_disponiveis(self):
        return self.__capacidade - len(self.__participantes)

    def get_participantes(self):
        return list(self.__participantes) #Gera uma lista, uma copia do original
    
    @staticmethod
    def validar_data_futura(data_str, formato='%d-%m-%Y %H:%M'):
        agora = datetime.now()

        try:
            data_evento = datetime.strptime(data_str, formato)
        except ValueError:
            raise ValueError(f"Formato de data inválido. Use o formato: {formato}")

        if data_evento < agora:
            raise ValueError("A data do evento não pode ser anterior à data atual.")
            
        return data_evento

    # Método de inscrição
    def inscrever(self, participante):
        if self.get_vagas_disponiveis() <= 0:
            return False, "Evento Lotado"

        if participante.get_email() in [p.get_email() for p in self.__participantes]:
            return False, "Participante já inscrito!"

        self.__participantes.append(participante)
        return True, "Inscrição realizada!"
    
    def cancelar_inscricao(self, email):
        """
        Remove um participante da lista pelo e-mail.
        """
        for p in self.__participantes:
            if p.get_email() == email:
                self.__participantes.remove(p)
                return True, "Inscrição cancelada com sucesso."
        return False, "Participante não encontrado."

    def calcular_receita(self):
        """
        Calcula receita total: número de participantes * preço do ingresso.
        """
        return len(self.__participantes) * self.__preco

    def contar_presentes(self):
        return sum(1 for p in self.__participantes if hasattr(p, "is_presente") and p.is_presente())
    

    # Adioncei  total inscritos, presentes e receita atual.
    def detalhes(self):
        return (f"Detalhes do Evento:\n"
                f"Nome: {self.get_nome()}\n"
                f"Data: {self.get_data()}\n"
                f"Local: {self.get_local()}\n"
                f"Categoria: {self.get_categoria()}\n"
                f"Preço: R$ {self.get_preco():.2f}\n"  # Formata o preço com 2 casas decimais
                f"Vagas Disponíveis: {self.get_vagas_disponiveis()}\n"
                f"Total Inscritos: {len(self.__participantes)} \n"
                f"Presentes: {self.contar_presentes()} \n"
                f"Receita atual (R$): {self.calcular_receita():.2f} \n")

                
            
