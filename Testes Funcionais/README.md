# Testes Funcionais (Trabalho 2)

Atividade da disciplina **Engenharia de Software III**: verificar, **pela interface web
e como um usuário faria**, se o sistema cumpre suas regras de negócio. Um robô
(Selenium) abre o Chrome, preenche campos, clica e confere o resultado na tela.

## Equipe

| Nome | Matrícula | Parte principal |
|---|---|---|
| _preencher_ | | |
| _preencher_ | | |
| _preencher_ | | |

## Estrutura

```
Testes Funcionais/
├── README.md                  este arquivo
├── requirements.txt           bibliotecas dos testes
├── pacote-A/                  Sabor Express + Matrícula Acadêmica (http://localhost:5000)
│   ├── sistema/app.py         sistema-alvo fornecido pelo professor
│   ├── exemplo/               exemplo resolvido: fluxo de pedido (CT01–CT05)
│   └── desafio/               DESAFIO A: portal de matrícula (CT01–CT13)
├── pacote-B/                  Biblioteca + Minicursos (próxima etapa)
├── projeto-anterior/          Sistema de Reserva de Laboratórios (próxima etapa)
└── resultados/                relatórios HTML, prints e registro das 3 execuções
```

## Preparação (uma vez)

Requisitos: Python 3.11+ e Google Chrome. Na primeira execução, o Selenium Manager
baixa o driver do Chrome sozinho (precisa de internet nessa primeira vez).

```bash
cd "Testes Funcionais"
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS:        source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip freeze > resultados/versoes_utilizadas.txt
```

## Pacote A: como rodar

**Terminal 1**, para subir o sistema:

```bash
cd "Testes Funcionais/pacote-A/sistema"
python app.py                      # http://localhost:5000
```

**Terminal 2** (com o mesmo `.venv` ativado), para rodar os testes:

```bash
# Exemplo resolvido (fluxo de pedido da lanchonete)
cd "Testes Funcionais/pacote-A/exemplo"
pytest -v --html=../../resultados/pacote-A/exemplo.html --self-contained-html

# Desafio A (portal de matrícula)
cd "../desafio"
pytest -v --html=../../resultados/pacote-A/desafio_execucao1.html --self-contained-html
```

Para rodar sem abrir a janela do Chrome:
- Linux/macOS: `HEADLESS=1 pytest -v`
- PowerShell: `$env:HEADLESS="1"; pytest -v`

> Rode sempre **em sequência** (sem `-n`/xdist). O estado do sistema fica em memória
> e é compartilhado. Cada teste já zera os dados com `POST /api/admin/reset`.

Detalhes do Desafio A (regras, casos e decisões) estão em
[`pacote-A/desafio/README.md`](pacote-A/desafio/README.md).
