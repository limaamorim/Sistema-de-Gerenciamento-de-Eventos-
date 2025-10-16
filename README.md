# Sistema de Gerenciamento de Eventos

Um projeto em Python para gerenciar eventos (Eventos, Palestras e Workshops), com persistência em arquivos JSON, autenticação de usuários (incluindo administrador), inscrição de participantes, check-in e relatórios simples.

> **Linguagem:** Python 3.8+

---

## Funcionalidades

* Cadastro e autenticação de usuários (usuários comuns e administradores).
* Cadastro de eventos gerais, palestras e workshops (com campos extras específicos).
* Listagem, busca por categoria e intervalo de datas.
* Inscrição e cancelamento de participantes.
* Check-in disponível no dia do evento.
* Persistência em JSON (`data/eventos.json` e `data/usuarios.json`).
* Relatórios com número de inscritos, vagas e receita.

---

## Estrutura do projeto

```
├── main.py                      # Entrada do programa (CLI)
├── sistema/                     # Lógica do sistema
│   ├── sistema_eventos.py       # Regras e operações do sistema
│   └── autenticador.py          # Login / cadastro de usuários
├── models/                      # Modelos de domínio
│   ├── evento.py                # Classe base Evento
│   ├── palestra.py              # Subclasse Palestra
│   ├── workshop.py              # Subclasse Workshop
│   ├── usuario.py               # Usuário comum
│   └── admin.py                 # Administrador (separado)
├── data/                        # Arquivos JSON gerados (não comitados por padrão)
│   ├── eventos.json
│   └── usuarios.json
│   └── persistencia_json.py     # Salva/carrega eventos em JSON
│    └── persistencia_usuarios.py# Salva/carrega usuários em JSON
├── tests/                       # Testes unitários
│   └── test_sistema_eventos.py
├── cores.py                     # Constantes para cores no terminal (opcional)
└── README.md                    # (este arquivo)
```

> Observação: os arquivos podem estar organizados em subpastas `sistema/`, `models/` e `data/` — ajuste conforme sua cópia local.

---


## Como rodar (local)

1. Clone o repositório para sua máquina.

2. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

4. Execute o aplicativo (CLI):

```bash
python main.py
```

O sistema criará os arquivos JSON na pasta `data/` automaticamente.

---

## Testes

Se quiser rodar os testes automáticos incluídos (usa `unittest`):

```bash
python -m unittest discover -v
```

Ou execute o arquivo de teste diretamente:

```bash
python tests/test_sistema_eventos.py
```

Se preferir `pytest` (instale-o primeiro), execute:

```bash
pytest -q
```

---

## Observações e boas práticas

* **Não** versionar arquivos de dados (`data/eventos.json`, `data/usuarios.json`). Adicione `data/` ao `.gitignore`.
* Mantenha uma conta de administrador inicial (o sistema cria um admin padrão caso não exista):

  * `admin@evento.com` / `1234`
* O projeto é orientado a objetos — você pode transformar as classes em uma API (FastAPI/Flask) sem muita mudança.

---

## Exemplo rápido

1. Rode `python main.py`.
2. Cadastre um usuário ou faça login como admin padrão.
3. Cadastre eventos, inscreva participantes e gere relatórios.

---

