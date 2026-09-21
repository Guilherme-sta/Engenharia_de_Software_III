# Testes Estáticos 

Revisão estática aplicada sobre a funcionalidade **US03 — Solicitar Reserva**
do projeto **Sistema de Reserva de Laboratórios** (Engenharia de Software II
/ IFPI), sem executar o sistema: revisão manual do requisito, da história
(INVEST), dos critérios de aceitação e do código, complementada por análise
automática com **Ruff**.

Atividade da disciplina **Engenharia de Software III**:
Registro A (revisão manual, 5 itens), Registro B (ferramenta, até 3 alertas)
e correção de problemas reais com reanálise e verificação de regressão.

Versão do código-fonte original analisada: repositório
[`NicolasDamasceno/Sistema-Reserva-Laboratorio`](https://github.com/NicolasDamasceno/Sistema-Reserva-Laboratorio),
pasta `app/`.

Este README documenta como reproduzir, na sua máquina, os dois relatórios do
Ruff (`relatorio-antes.txt` e `relatorio-depois.txt`), aplicar as duas
correções e confirmar que a suíte de testes não regrediu — exatamente os
resultados descritos em `relatorio-testes-estaticos.md`.

---

## Estrutura deste pacote

```
.
├── README.md
├── relatorio-testes-estaticos.md   # relatório completo (artefatos + Registro A + Registro B + correções)
├── relatorio-antes.txt             # saída do Ruff sobre o código original
├── relatorio-depois.txt            # saída do Ruff após as correções
├── versao-original/                # cópia intacta do projeto, antes de qualquer alteração
└── app/, tests/, data/, docs/...   # projeto já com as duas correções aplicadas
```

> A pasta `versao-original/` existe só para comparação. Para rodar a
> análise "antes" você mesmo, use o código de lá; para reproduzir o
> "depois", use o `app/` da raiz, que já está corrigido.

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

Na pasta raiz do projeto:

```powershell
python -m venv venv
```

### 2.2. Ativar o ambiente virtual

No Windows, o caminho do script de ativação normalmente é
`venv\Scripts\Activate.ps1`. Dependendo da instalação do Python, ele pode
aparecer em `venv\bin\Activate.ps1` em vez disso — se o primeiro caminho não
existir, use o segundo.

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
pip install ruff fastapi pytest httpx
```

`ruff` é a ferramenta de análise estática da atividade. `fastapi`, `pytest`
e `httpx` são as dependências do próprio projeto, necessárias para rodar a
suíte de testes (`tests/test_reservas.py`, `tests/test_laboratorios.py`).

Confira a versão do Ruff — ela entra no Registro B do relatório:

```powershell
python -m ruff --version
```

Saída esperada: `ruff 0.16.7` (ou próxima).

---

## 3. Rodando a análise "antes" (sobre `versao-original/`)

Entre em `versao-original/` e rode o Ruff com as mesmas duas regras usadas
na atividade — importações sem uso (`F401`) e variáveis locais sem uso
(`F841`):

```powershell
cd versao-original
python -m ruff check app --isolated --select F401,F841 --output-file relatorio-antes.txt
```

- `--isolated` ignora qualquer configuração de outro arquivo do projeto, para
  o resultado ser reprodutível na máquina de qualquer integrante do grupo.
- Não use `--fix` nesta etapa: o Registro B exige o relatório **antes** de
  qualquer correção.

Saída esperada em `relatorio-antes.txt`: **2 alertas**, ambos F401 —
`fastapi.status` sem uso em `app/routers/reserva_router.py` e
`datetime.date` sem uso em `app/schemas/reserva_schema.py`.

Para ver o terceiro alerta citado no relatório (F811, que explica por que o
`date` do topo aparece como "sem uso"):

```powershell
python -m ruff check app --isolated --select F811
```

---

## 4. Aplicando as correções

Volte para a raiz do pacote (`cd ..`) e trabalhe sobre a pasta `app/` — ela
já está com as duas correções aplicadas; esta seção explica cada uma, caso
o grupo queira refazer manualmente sobre o próprio repositório.

### 4.1. Remover as importações sem uso (origem: ferramenta)

`app/routers/reserva_router.py`, linha 1:

```diff
- from fastapi import APIRouter, Depends, HTTPException, status
+ from fastapi import APIRouter, Depends, HTTPException
```

`app/schemas/reserva_schema.py`, dentro de `validar_data`:

```diff
      def validar_data(cls, valor: str):
-         from datetime import date
          data_obj = date.fromisoformat(valor)
```

### 4.2. Centralizar a regra de sobreposição de horário (origem: revisão manual)

A regra estava duplicada, com sinais invertidos, em
`reserva_service.py` e em `laboratorio_services.py` (arquivo morto, sem
nenhum import em todo o projeto). Criar `app/services/regras_horario.py`:

```python
def ha_sobreposicao(inicio_a: str, fim_a: str, inicio_b: str, fim_b: str) -> bool:
    """RN-03: dois intervalos HH:MM se sobrepoem quando nenhum termina
    antes (ou no momento) do inicio do outro."""
    return not (fim_a <= inicio_b or inicio_a >= fim_b)
```

Depois:

- em `reserva_service.py`, trocar a expressão do `if not (...)` por uma
  chamada a `ha_sobreposicao(...)`;
- mover `verificar_disponibilidade` para `laboratorio_service.py` (o service
  que o router realmente usa), também chamando `ha_sobreposicao(...)`;
- apagar `app/services/laboratorio_services.py`.

Os diffs completos estão em `relatorio-testes-estaticos.md`, seção 5.

---

## 5. Rodando a análise "depois" e a reanálise

Na pasta raiz (com o `app/` já corrigido):

```powershell
python -m ruff check app --isolated --select F401,F841 --output-file relatorio-depois.txt
```

Saída esperada: `All checks passed!`

---

## 6. Rodando a suíte de testes (verificação de regressão)

Ainda na raiz do pacote, com o ambiente virtual ativado:

```powershell
python -m pytest -q
```

Saída esperada: **13 passed, 1 failed**. A falha
(`test_cancelar_reserva_sucesso`) é **pré-existente** — já acontecia antes
das duas correções — e está documentada em `relatorio-testes-estaticos.md`
como achado registrado e não corrigido (divergência entre o teste, que
manda o solicitante por query string, e o endpoint, que espera o corpo da
requisição).

Para confirmar que a falha já existia antes das correções, rode o mesmo
comando dentro de `versao-original/`:

```powershell
cd versao-original
python -m pytest -q
```

O resultado deve ser idêntico: 13 passed, 1 failed, mesma falha.

> **Importante:** rode sempre o pytest a partir da **raiz** de cada cópia do
> projeto (`versao-original/` ou a raiz principal), nunca de dentro de
> `tests/`. O `reserva_repo.py` usa o caminho relativo `data/reservas.json`
> e não encontra o arquivo se você estiver em outra pasta.

---

## 7. Resumo dos alertas do Registro B

| ID | Regra | Arquivo/linha | Decisão |
|---|---|---|---|
| B-01 | F401 — unused-import | `reserva_router.py:1` | Corrigir |
| B-02 | F401 — unused-import | `reserva_schema.py:4` | Corrigir |
| B-03 | F811 — redefined-while-unused | `reserva_schema.py:18` | Corrigir (mesma alteração de B-02) |

Detalhes de cada alerta — significado e evidência — e o Registro A completo
(revisão manual dos 5 itens: nomes, regras de negócio, entradas/retornos,
repetição, tratamento de erros) estão em `relatorio-testes-estaticos.md`.

---

## 8. Solução de problemas comuns

- **`'ruff' não é reconhecido...` ou `'pytest' não é reconhecido...`** — o
  ambiente virtual não está ativado, ou a instalação do passo 2.3 falhou
  antes de terminar. Confirme que o prompt mostra `(venv)` e rode
  `pip install ruff fastapi pytest httpx` novamente, conferindo se todos os
  pacotes terminaram com "Successfully installed".
- **`venv\Scripts\Activate.ps1` não existe** — use `venv\bin\Activate.ps1`
  em vez disso (algumas instalações do Python no Windows criam a pasta
  `bin` em vez de `Scripts`).
- **Erro de política de execução de scripts (`...não pode ser carregado
  porque a execução de scripts foi desabilitada...`)** — rode
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` e tente
  ativar o ambiente de novo.
- **O Ruff encontra alertas diferentes dos descritos aqui** — confirme que
  está usando `--isolated --select F401,F841` exatamente como nos comandos
  acima; sem essas opções, o Ruff aplica seu conjunto de regras padrão (bem
  mais amplo) e/ou lê configurações de outros arquivos do projeto.
- **`ModuleNotFoundError` ao rodar o pytest** — confirme que está na pasta
  raiz correta (a que contém `app/`, `tests/` e `data/`), e não dentro de
  `tests/` ou `app/`.