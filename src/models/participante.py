class Participante:
    def __init__(self, nome, email, checkin=0):
        self.__nome = nome
        self.__email = email
        self.__checkin = checkin  # novo atributo

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_checkin(self):
        return self.__checkin

    def set_checkin(self):
        self.__checkin = 1
