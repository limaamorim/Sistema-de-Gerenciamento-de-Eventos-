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
