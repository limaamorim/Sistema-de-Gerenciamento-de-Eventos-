# Arquivo: data/persistencia_json.py (Versão Final e Corrigida)

import json
import os
from datetime import datetime
from models.evento import Evento
from models.palestra import Palestra
from models.workshop import Workshop
from models.usuario import Usuario 

ARQUIVO_JSON = "data/eventos.json"
os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)

class PersistenciaJSON:
    @staticmethod
    def salvar(eventos):
        dados = []
        for e in eventos:
            tipo = e.__class__.__name__
            participantes = [
                {
                    "nome": p.get_nome(),
                    "email": p.get_email(),
                    "tipo": p.get_tipo(),
                    "checkin": p.get_checkin()
                }
                for p in e.get_participantes()
            ]

            extra = None
            if tipo == "Workshop":
                extra = {
                    "materiais": e.get_material(),
                    "instrutor": e.get_instrutor()
                }
            elif tipo == "Palestra":
                extra = e.get_palestrante()

            dados.append({
                "tipo": tipo,
                "nome": e.get_nome(),
                "data": e.get_data(),
                "hora": e.get_hora(),
                "local": e.get_local(),
                "capacidade": e.get_vagas_disponiveis() + len(e.get_participantes()),
                "categoria": e.get_categoria(),
                "preco": e.get_preco(),
                "extra": extra,
                "participantes": participantes
            })

        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar():
        eventos = []
        if not os.path.exists(ARQUIVO_JSON):
            return eventos

        # Tratamento para arquivo vazio
        if os.path.getsize(ARQUIVO_JSON) == 0:
            return eventos

        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            try:
                dados = json.load(arquivo)
            except json.JSONDecodeError:
                return []

        for item in dados:
            tipo = item["tipo"]
            data_str = item["data"].replace("-", "/")
            data_evento = datetime.strptime(data_str, "%d/%m/%Y")
            hora_evento = datetime.strptime(item["hora"], "%H:%M").time()

            if tipo == "Workshop":
                evento = Workshop(
                    item["nome"], data_evento, hora_evento,
                    item["local"], item["capacidade"], item["categoria"],
                    item["preco"],
                    item["extra"]["materiais"],
                    item["extra"]["instrutor"]
                )
            elif tipo == "Palestra":
                evento = Palestra(
                    item["nome"], data_evento, hora_evento,
                    item["local"], item["capacidade"], item["categoria"],
                    item["preco"], item["extra"]
                )
            else:
                evento = Evento(
                    item["nome"], data_evento, hora_evento,
                    item["local"], item["capacidade"], item["categoria"], item["preco"]
                )
            
            for p in item.get("participantes", []):
                participante = Usuario(p["nome"], p["email"], "", p.get("tipo", "user"))
                
                if p.get("checkin", False):
                    participante.fazer_checkin()

                evento.inscrever(participante)

            eventos.append(evento)

        return eventos