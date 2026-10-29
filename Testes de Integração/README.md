# Testes de Integração

Atividade da disciplina **Engenharia de Software III**: compreender os níveis de
teste de software e aplicar testes em **nível de integração**, ou seja, testes que
verificam a comunicação real entre dois ou mais componentes, sem isolar tudo com
dublês (mocks/stubs).

A atividade tem duas partes:

1. **`estoque/`**: trabalho prático do roteiro (Sistema de Controle de Estoque),
   em Python (pytest + sqlite3 em memória).
2. **`reserva_laboratorio/`**: trabalho complementar. Testes de integração
   aplicados a um trecho do projeto **Sistema de Reserva de Laboratórios**
   (Engenharia de Software II / IFPI), repositório
   [`NicolasDamasceno/Sistema-Reserva-Laboratorio`](https://github.com/NicolasDamasceno/Sistema-Reserva-Laboratorio).

---

## Estrutura deste pacote

```
.
├── README.md
├── requirements.txt
├── estoque/
│   ├── produto.py                # classes fornecidas pelo roteiro
│   ├── produto_repository.py
│   ├── estoque_service.py
│   └── test_estoque_service_integration.py
└── reserva_laboratorio/
    ├── pytest.ini
    ├── app/                      # trecho extraído do projeto original
    │   ├── models/               # Reserva, Laboratorio
    │   ├── schemas/              # ReservaCriar, AvaliarReserva (Pydantic)
    │   ├── repositories/         # ReservaRepository, LaboratorioRepository (JSON)
    │   ├── services/             # ReservaService
    │   └── exceptions/
    └── tests/
        └── test_integracao_reserva.py
```

---

## 1. Pré-requisitos

- **Python 3.10 ou superior** e **pip**

```powershell
python --version
```

---

## 2. Preparando o ambiente Python

Na raiz desta pasta (`Testes de Integração/`):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Instala só o `pytest` e o `pydantic` (usado pelos schemas do projeto de
reservas). Se o `Activate.ps1` não existir em `venv\Scripts`, use
`venv\bin\Activate.ps1`. Se aparecer erro de política de execução, rode
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` e tente de novo.

---

## 3. Parte 1: Sistema de Controle de Estoque

### 3.1. Rodando

```powershell
cd estoque
pytest -v
```

Saída esperada:

```
test_adicionar_estoque_atualiza_banco PASSED
test_vender_produto_com_estoque_suficiente PASSED
test_vender_produto_com_estoque_insuficiente_nao_altera_banco PASSED
test_vender_quantidade_invalida_nao_altera_banco[zero] PASSED
test_vender_quantidade_invalida_nao_altera_banco[negativa] PASSED
test_vender_quantidade_invalida_nao_altera_banco[maior_que_estoque] PASSED

6 passed
```

### 3.2. Testes implementados

| Teste | Cenário |
|---|---|
| `test_adicionar_estoque_atualiza_banco` | adicionar estoque persiste no banco (10 + 5 = 15) |
| `test_vender_produto_com_estoque_suficiente` | venda com estoque suficiente (10 − 3 = 7) |
| `test_vender_produto_com_estoque_insuficiente_nao_altera_banco` | estoque insuficiente lança exceção e NÃO altera o banco |
| `test_vender_quantidade_invalida_nao_altera_banco` | **desafio extra**: teste parametrizado com venda zero, negativa e maior que o estoque |

### 3.3. Observações

- **Banco do zero a cada teste.** A fixture `conexao` abre
  `sqlite3.connect(":memory:")`, cria a tabela, insere um produto com 10
  unidades e fecha a conexão no final, descartando o banco.
- **Bug encontrado pelo desafio extra.** O `vender_produto` fornecido
  aceitava vender `0` (não fazia nada) e vender `-5` (o estoque **aumentava**
  para 15). Foi adicionada uma validação mínima (`quantidade <= 0` lança
  `ValueError`), marcada com comentário no código.

---

## 4. Parte 2: Sistema de Reserva de Laboratórios (trabalho complementar)

```powershell
cd reserva_laboratorio
pytest -v
```

Saída esperada:

```
tests/test_integracao_reserva.py::test_solicitar_reserva_grava_no_arquivo_como_pendente PASSED
tests/test_integracao_reserva.py::test_aprovar_reserva_persiste_status_aprovada PASSED
tests/test_integracao_reserva.py::test_aprovar_com_conflito_lanca_excecao_e_nao_altera_arquivo PASSED
tests/test_integracao_reserva.py::test_solicitar_em_laboratorio_inativo_nao_grava_reserva PASSED
tests/test_integracao_reserva.py::test_fluxo_reserva_aprovada_bloqueia_nova_solicitacao_no_mesmo_horario PASSED

5 passed
```

### 4.1. Componentes integrados

```
teste  →  ReservaService  →  ReservaRepository / LaboratorioRepository  →  arquivos JSON
```

No projeto original, os repositórios persistem os dados em `data/reservas.json`
e `data/laboratorios.json`; esses arquivos são o "banco de dados" do sistema.
O código em `app/` foi copiado **sem alteração** do projeto original. Só ficaram
de fora as partes que não participam dessa comunicação (FastAPI, routers e
`LaboratorioService`).

### 4.2. Como a dependência externa foi isolada

Cada teste recebe uma pasta temporária nova (`tmp_path` do pytest), cria nela
arquivos JSON com dados controlados e, via `monkeypatch`, faz os repositórios
gravarem ali em vez de em `data/`. É o equivalente ao banco em memória do
exemplo do estoque: o arquivo é real, mas é criado do zero a cada teste e
descartado no final. Os testes não dependem uns dos outros, e os dados reais
do sistema nunca são tocados.

As asserções leem o arquivo JSON **direto do disco**, sem passar pelo service
nem pelo repositório.

### 4.3. Casos de teste

| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| IT-01 | Solicitar reserva em laboratório ativo | caminho feliz | reserva gravada no JSON com status `pendente`, `id` e `data_hora_solicitacao` preenchidos pelo repositório |
| IT-02 | Aprovar reserva pendente | caminho feliz | status `aprovada` persistido no JSON |
| IT-03 | Aprovar reserva cujo horário conflita com outra já aprovada | **caminho de erro** | `ConflitoDeHorario` é lançada e o arquivo continua **byte a byte igual** |
| IT-04 | Solicitar reserva em laboratório inativo (status lido do JSON de laboratórios) | **caminho de erro** | `OperacaoNaoPermitida` é lançada e nenhuma reserva é gravada |
| IT-05 | Fluxo: solicitar → aprovar → nova solicitação no mesmo horário | fluxo completo | a segunda solicitação é barrada; só a primeira fica no arquivo |

O IT-03 é o equivalente direto do "estoque insuficiente" do roteiro: a regra
de negócio recusa a operação **e** o estado persistido não muda.

### 4.4. Por que isto é teste de integração e não teste unitário

Na atividade de Caixa Branca, o `ReservaService` foi testado com um
`FakeReservaRepository` (um stub em memória): aquilo era **teste unitário**,
porque provava só a lógica do `_verificar_conflito`, isolada.

Aqui nada é substituído: o teste chama o `ReservaService` real, que usa os
repositórios reais, que serializam os models (`to_dict` / `from_dict`) e leem e
gravam arquivos reais. Por isso, esses testes pegam defeitos que um teste
unitário com stub não pega. Exemplo verificado: se o `Reserva.to_dict()`
gravar o status errado no JSON, a lógica do service continua "certa" e o teste
unitário continua passando, mas **IT-02 e IT-05 falham**, porque o status lido
de volta do arquivo não é o esperado.

---

## 5. Solução de problemas comuns

- **`ModuleNotFoundError: No module named 'app'`**: rode o pytest de dentro
  da pasta `reserva_laboratorio/` (é ali que está o `pytest.ini` que coloca
  `app` no caminho).
- **`ModuleNotFoundError: No module named 'pydantic'`**: o ambiente virtual
  não está ativo ou o `pip install -r requirements.txt` não terminou.
- **Erro de data passada no `ReservaCriar`**: o schema do projeto recusa
  datas anteriores a hoje; os testes usam `2030-05-20` de propósito.
- **`ModuleNotFoundError: No module named 'estoque_service'`**: rode o
  pytest de dentro da pasta `estoque/`.
