import json
import os
from datetime import datetime
from models.evento import Evento
from models.palestra import Palestra
from models.workshop import Workshop
from models.participante import Participante

ARQUIVO_JSON = "data/eventos.json"
os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)

class PersistenciaJSON:
    @staticmethod
    def salvar(eventos):
        """Salva todos os eventos e participantes em um arquivo JSON."""
        dados = []
        for e in eventos:
            tipo = e.__class__.__name__
            participantes = [
                {"nome": p.get_nome(), "email": p.get_email(), "checkin": p.get_checkin()}
                for p in e.get_participantes()
            ]

            extra = None
            if tipo == "Workshop":
                extra = e.get_material()
            elif tipo == "Palestra":
                extra = e.get_palestrante()

            dados.append({
                "tipo": tipo,
                "nome": e.get_nome(),
                "data": e.get_data(),
                "local": e.get_local(),
                "capacidade": e.get_vagas_disponiveis() + len(e.get_participantes()),
                "categoria": e.get_categoria(),
                "preco": e.get_preco(),
                "extra": extra,
                "participantes": participantes
            })

        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    # ============================================================
    @staticmethod
    def carregar():
        """Carrega todos os eventos e participantes do arquivo JSON."""
        eventos = []
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                tipo = item["tipo"]
                data_evento = datetime.strptime(item["data"], "%m-%d")
                if tipo == "Workshop":
                    evento = Workshop(item["nome"], data_evento, item["local"], item["capacidade"],
                                      item["categoria"], item["preco"], item["extra"])
                elif tipo == "Palestra":
                    evento = Palestra(item["nome"], data_evento, item["local"], item["capacidade"],
                                      item["categoria"], item["preco"], item["extra"])
                else:
                    evento = Evento(item["nome"], data_evento, item["local"], item["capacidade"],
                                    item["categoria"], item["preco"])

                for p in item["participantes"]:
                    participante = Participante(p["nome"], p["email"], p["checkin"])
                    evento.inscrever(participante)

                eventos.append(evento)

        except FileNotFoundError:
            pass

        return eventos
