# Testes de Caixa Branca — `ReservaService._verificar_conflito`

Testes estruturais (caixa branca) aplicados sobre o método `_verificar_conflito`
da classe `ReservaService`, do projeto **Sistema de Reserva de Laboratórios**
(Engenharia de Software II / IFPI).

Atividade da disciplina **Engenharia de Software III**: construção do Grafo de
Fluxo de Controle, cálculo da complexidade ciclomática, definição de caminhos
básicos e implementação dos casos de teste correspondentes.

Commit do código-fonte original analisado:
`edec87d23b5600ac0b2150434967e7272a8b73a6` — repositório
[`NicolasDamasceno/Sistema-Reserva-Laboratorio`](https://github.com/NicolasDamasceno/Sistema-Reserva-Laboratorio).

Este README documenta como rodar a **suíte isolada** (`isolated/`) — uma cópia
fiel da lógica de `_verificar_conflito`, extraída sem alteração de
comportamento e sem nenhuma dependência externa (não precisa do FastAPI, do
Pydantic nem do restante do projeto). É a forma mais simples e rápida de
reproduzir os 9 casos de teste e a cobertura de 100% descritas no relatório.

---

## Estrutura deste pacote

```
.
├── README.md
├── requirements.txt
├── isolated/
│   ├── conflito_unit.py    # lógica extraída de _verificar_conflito
│   └── test_isolated.py    # os 9 casos de teste (CT-01 a CT-09)
├── tests/
│   └── test_verificar_conflito_caixa_branca.py   # suíte alternativa, roda contra o projeto completo (não coberta por este README)
└── docs/
```

> A pasta `tests/` contém uma segunda suíte que testa o método real dentro
> do projeto completo (com FastAPI/Pydantic). Ela não é necessária para
> validar os resultados do relatório — este README cobre apenas a suíte
> isolada, que já é suficiente.

---

## 1. Pré-requisitos

- **Python 3.10 ou superior**
- **pip**

Verifique sua versão do Python:

```powershell
python --version
```

---

## 2. Preparando o ambiente

### 2.1. Criar o ambiente virtual

```powershell
python -m venv venv
```

### 2.2. Ativar o ambiente virtual

No Windows, o caminho do script de ativação normalmente é `venv\Scripts\Activate.ps1`.
Dependendo da instalação do Python, ele pode aparecer em `venv\bin\Activate.ps1`
em vez disso — se o primeiro caminho não existir, use o segundo.

```powershell
.\venv\Scripts\Activate.ps1
```

Se aparecer um erro de política de execução de script bloqueada, rode uma
vez (vale só para essa janela do terminal):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

e tente ativar de novo. Você saberá que o ambiente está ativo quando o
prompt passar a mostrar `(venv)` no início da linha.

### 2.3. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
pip install -r requirements.txt
```

Isso instala apenas `pytest`, `pytest-cov`, `coverage` e `radon` — o
suficiente para a suíte isolada. Não é preciso instalar FastAPI nem Pydantic.

---

## 3. Rodando os testes

Entre na pasta `isolated/` e rode o pytest:

```powershell
cd isolated
pytest test_isolated.py -v
```

Saída esperada:

```
test_isolated.py::test_ct01 PASSED
test_isolated.py::test_ct02 PASSED
test_isolated.py::test_ct03 PASSED
test_isolated.py::test_ct04 PASSED
test_isolated.py::test_ct05 PASSED
test_isolated.py::test_ct06 PASSED
test_isolated.py::test_ct07 PASSED
test_isolated.py::test_ct08 PASSED
test_isolated.py::test_ct09 PASSED

9 passed
```

---

## 4. Gerando o relatório de cobertura (linhas e ramos)

Ainda dentro da pasta `isolated/`:

```powershell
pytest test_isolated.py --cov=conflito_unit --cov-branch --cov-report=term-missing
```

Resultado esperado: **100% de cobertura de linhas e 100% de cobertura de
ramos** (branches), sem nenhuma linha faltante — confirmando que os 8
caminhos básicos do Grafo de Fluxo de Controle (ver `docs/grafo_fluxo_controle.png`)
foram todos exercitados.

```
Name               Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------
conflito_unit.py      17      0     10      0   100%
--------------------------------------------------------------
TOTAL                 17      0     10      0   100%
```

### 4.1. Relatório em HTML (opcional)

Para visualizar a cobertura linha a linha no navegador:

```powershell
pytest test_isolated.py --cov=conflito_unit --cov-branch --cov-report=html:htmlcov
```

Isso cria a pasta `htmlcov/`; abra `htmlcov/index.html` no navegador.

---

## 5. Calculando a complexidade ciclomática (radon)

Para conferir o valor de V(G) = 8 calculado manualmente no relatório:

```powershell
radon cc conflito_unit.py -s -a
```

Saída esperada:

```
conflito_unit.py
    F 9:0 verificar_conflito - B (8)
    C 3:0 StatusReserva - A (1)

2 blocks (classes, functions, methods) analyzed.
Average complexity: A (4.5)
```

A linha relevante é a primeira: `verificar_conflito - B (8)`, confirmando o
mesmo valor calculado manualmente no relatório (V(G) = 8). A segunda linha
é apenas o enum `StatusReserva` também presente no arquivo, sem relevância
para esta análise.

---

## 6. Resumo dos 9 casos de teste

| ID | Cenário resumido | Resultado esperado |
|---|---|---|
| CT-01 | Reserva aprovada, mesma data, horários sobrepostos | `True` (conflito) |
| CT-02 | Nenhuma reserva cadastrada (laço com zero iterações) | `False` |
| CT-03 | `excluir_id` de outra reserva; a reserva conflitante não é ignorada | `True` |
| CT-04 | `excluir_id` igual ao id da própria reserva sobreposta | `False` |
| CT-05 | Reserva existente com status `PENDENTE` (não aprovada) | `False` |
| CT-06 | Reserva aprovada, porém em data diferente | `False` |
| CT-07 | Mesma data; novo horário termina antes do existente começar | `False` |
| CT-08 | Mesma data; novo horário começa depois do existente terminar | `False` |
| CT-09 | Duas reservas: a primeira é ignorada, a segunda gera conflito (mais de uma iteração do laço) | `True` |

Detalhes de cada caso — caminho do Grafo de Fluxo de Controle exercitado e
critério de cobertura atendido — estão descritos no relatório completo da
atividade (documento `.docx` entregue em separado).

---

## 7. Solução de problemas comuns

- **`'pytest' não é reconhecido...`** — o ambiente virtual não está ativado,
  ou a instalação do passo 2.3 falhou antes de terminar. Confirme que o
  prompt mostra `(venv)` e rode `pip install -r requirements.txt` novamente,
  conferindo se todos os pacotes terminaram com "Successfully installed".
- **`venv\Scripts\Activate.ps1` não existe** — use `venv\bin\Activate.ps1`
  em vez disso (algumas instalações do Python no Windows criam a pasta
  `bin` em vez de `Scripts`).
- **Erro de política de execução de scripts (`...não pode ser carregado
  porque a execução de scripts foi desabilitada...`)** — rode
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` e tente
  ativar o ambiente de novo.
- **`ModuleNotFoundError: No module named 'conflito_unit'`** — confirme que
  você está dentro da pasta `isolated/` ao rodar o pytest (`cd isolated`).
