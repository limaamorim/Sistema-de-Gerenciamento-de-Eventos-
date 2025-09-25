usecaseDiagram
  actor Participante
  actor Administrador
  actor Organizador

  rectangle Sistema {
    (Cadastrar Evento)
    (Inscrever Participante)
    (Cancelar Inscrição)
    (Check-in)
    (Listar Eventos)
    (Gerar Relatório)
  }

  Administrador --> (Cadastrar Evento)
  Administrador --> (Gerar Relatório)
  Participante --> (Inscrever Participante)
  Participante --> (Cancelar Inscrição)
  Participante --> (Listar Eventos)
  Organizador --> (Check-in)
