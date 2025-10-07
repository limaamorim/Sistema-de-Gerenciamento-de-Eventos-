from models.evento import Evento

class Palestra(Evento):
    def __init__(self, nome, data, local, capacidade, categoria, preco, palestrante):
        super().__init__(nome, data, local, capacidade, categoria, preco)
        self.__palestrante = palestrante
    
    def get_palestrante(self):
        return self.__palestrante
    
    def detalhes(self):
        detalhes_palestra = super().detalhes()
        return f"{detalhes_palestra}Palestrante: {self.get_palestrante()}\n"
                
                
               