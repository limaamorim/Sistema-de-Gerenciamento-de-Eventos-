# Sistema de Gerenciamento de Eventos

## 📌 Diagrama de Classes UML
```mermaid
classDiagram
    class Evento {
        - nome : str
        - data : datetime
        - local : str
        - capacidade_maxima : int
        - categoria : str
        - preco : float
        + detalhes() str
    }
    class Workshop {
        - material_necessario : str
        + detalhes() str
    }
    class Palestra {
        - palestrante : str
        + detalhes() str
    }
    class Participante {
        - nome : str
        - email : str
        - checkin : bool
        + realizar_checkin()
    }

    Evento <|-- Workshop
    Evento <|-- Palestra
    Evento "1" --> "many" Participante

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

