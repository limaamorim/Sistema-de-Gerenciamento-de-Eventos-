def increver_participante(self, nome, email):
    if self.get_vagas_disponiveis() <= 0:
        return False, " Evento lotado. Não é possível inscrever mais participantes."

    for p in self.__participantes: 
        if p.get_email().lower() == email.lower():
            return False, " e-mail já escrito neste evento." 

    novo_participante = Participante(nome, email)
    self.__participantes.append(novo_participante)
    return True, f" {nome} inscrito com sucesso!"

def cancelar_inscricao(self, email):
    for p in self.__participantes:
        if p.get_email().lower() == email.lower():
            self.__participantes.remove(p)
            return True, f" Incrição de {p.get_nome()} cancelada com sucesso."
    return False, " e-mail não encontrado entre os participantes inscritos."

def fazer_check_in(self, email):
    for p in self.__participantes:
        if p.get_email().lower() == email.lower():
            if getattr(p, "check_in", False):
                return False, f" {p.get_nome()} já fez check-in."
            p.check_in = True
            return True, f" Check-in realizado com sucesso para {p.get_nome()}."
    return False, " Participante não encontrado para realizar check-in."


