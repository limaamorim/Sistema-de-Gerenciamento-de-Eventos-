    # workshop.py
from models.evento import Evento


class Workshop(Evento):
        def __init__(self, nome, data, local, capacidade, categoria, preco, material_necessario):
            super().__init__(nome, data, local, capacidade, categoria, preco)            
            self.__material_necessario = material_necessario
            
        def get_material(self):
            return self.__material_necessario

        def detalhes(self):
            detalhes_base = super().detalhes()
            return f"{detalhes_base}Material Necessário: {self.get_material()}\n"