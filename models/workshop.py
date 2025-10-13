    # workshop.py
from models.evento import Evento


class Workshop(Evento):
        def __init__(self, nome, data, hora, local, capacidade, categoria, preco, materiais, instrutor):
            super().__init__(nome, data, hora, local, capacidade, categoria, preco)            
            self.__materiais = materiais
            self.__instrutor = instrutor
            
        def get_material(self):
            return self.__materiais
        
        def get_instrutor(self):
            return self.__instrutor

        def detalhes(self):
            detalhes_base = super().detalhes()
            return (f"{detalhes_base}Material Necessário: {self.get_material()}\n"
                    f"Instrutor: {self.get_instrutor()}\n")