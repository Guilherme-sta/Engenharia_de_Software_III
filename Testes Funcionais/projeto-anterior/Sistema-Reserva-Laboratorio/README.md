# Sistema de Reserva de Laboratórios

API REST para gerenciamento de laboratórios e reservas, desenvolvida na disciplina **Engenharia de Software II** — IFPI TADS.

No Trabalho 2 de **Engenharia de Software III**, a API ganhou uma interface web mínima para automatizar com Selenium e pytest os fluxos de gestão de laboratórios e reserva de laboratórios.

## Equipe

| Nome | Matrícula | Responsabilidade principal |
|---|---|---|
| Guilherme Alves Barbosa | 2025111TADS0010 | Services (regras de negócio) |
| Marcos Gabriel Mendes Silva | 2024211TADS0007 | Routers, Schemas e Evidências |
| Nicolas Antônio Damasceno | 2025111TADS0023 | Repositories e Integração |

## Tecnologias e estrutura

- Python 3.11.9 no ambiente validado, FastAPI, Pydantic v2 e Uvicorn
- HTML, CSS e JavaScript com Fetch API
- pytest, HTTPX, Selenium, Chrome, ChromeDriver e pytest-html

```text
app/           API, rotas, esquemas, serviços, repositórios e modelos
data/          Persistência nos JSON de laboratórios e reservas
web/           Interface estática servida em /web/
tests/         14 testes HTTP com FastAPI TestClient
tests_ui/      8 testes Selenium, fixtures, Page Objects e matriz CSV
pytest.ini     Configuração do pytest
requirements.txt
ESCOPO_ESIII.md
```

## Preparação do ambiente

Use Python 3.11 ou superior e Chrome para a suíte de interface. No Git Bash, a partir da raiz do repositório, reutilize o ambiente virtual compartilhado. O primeiro comando só cria o ambiente se ele estiver ausente.

```bash
test -f "Testes Funcionais/.venv/Scripts/python.exe" || python -m venv "Testes Funcionais/.venv"
cd "Testes Funcionais/projeto-anterior/Sistema-Reserva-Laboratorio"
projeto="$PWD"
python_venv="$projeto/../../.venv/Scripts/python.exe"
"$python_venv" -m pip install -r requirements.txt
```

## API e interface web

Use as variáveis da preparação no mesmo terminal. O servidor roda em uma pasta temporária para que as operações de demonstração sejam gravadas em cópias dos JSON.

```bash
demo="$(mktemp -d)"
mkdir "$demo/data"
cp "$projeto/data/"{laboratorios,reservas}.json "$demo/data/"
(
  cd "$demo" || exit 1
  "$python_venv" -B -m uvicorn app.main:app --app-dir "$projeto" --host 127.0.0.1 --port 8000
)
```

Abra [a interface web](http://127.0.0.1:8000/web/) ou [a documentação Swagger](http://127.0.0.1:8000/docs). A página chama a API na mesma origem. Os repositórios gravam em `data/` relativo ao diretório de trabalho. Se o servidor iniciar na raiz do projeto, ele usará os JSON dessa pasta.

## Endpoints Disponíveis

### Laboratórios

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/laboratorios/` | Cadastrar laboratório |
| GET | `/laboratorios/` | Listar laboratórios |
| GET | `/laboratorios/{id}` | Buscar laboratório por ID |
| PUT | `/laboratorios/{id}` | Atualizar laboratório |

### Reservas

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/reservas/` | Solicitar reserva |
| GET | `/reservas/` | Listar reservas |
| GET | `/reservas/{id}` | Buscar reserva por ID |
| PATCH | `/reservas/{id}/avaliar` | Aprovar ou rejeitar reserva |
| PATCH | `/reservas/{id}/cancelar` | Cancelar reserva |

## Exemplo de Uso

**Cadastrar laboratório:**
```json
POST /laboratorios/
{
  "nome": "Laboratório de Redes",
  "capacidade": 30
}
```

**Solicitar reserva:**
```json
POST /reservas/
{
  "laboratorio_id": "<id-do-laboratorio>",
  "solicitante": "Guilherme",
  "data": "2027-08-10",
  "hora_inicio": "08:00",
  "hora_fim": "10:00"
}
```

**Aprovar reserva:**
```json
PATCH /reservas/{id}/avaliar
{
  "acao": "aprovar"
}
```

**Rejeitar reserva (justificativa obrigatória):**
```json
PATCH /reservas/{id}/avaliar
{
  "acao": "rejeitar",
  "justificativa": "Laboratório em manutenção"
}
```

**Cancelar reserva** com `PATCH /reservas/{id}/cancelar` e corpo JSON.

```json
{"solicitante": "Guilherme"}
```

## Testes originais da API

O `setup_function` sobrescreve ambos os JSON no início de cada caso. Execute os 14 testes em uma cópia isolada. As datas fixas de janeiro de 2027 nesses testes serão rejeitadas quando ficarem no passado.

```bash
copia_api="$(mktemp -d)"
cp -R "$projeto/"{app,data,tests,web} "$copia_api/"
cp "$projeto/pytest.ini" "$copia_api/"
(
  cd "$copia_api" || exit 1
  "$python_venv" -B -m pytest tests/ -v -p no:cacheprovider
)
```

## Testes funcionais Selenium

Execute na pasta do projeto. O Chrome abre em modo headless por padrão. Use `HEADLESS=0` para abrir uma janela. Se o Selenium Manager não resolver o driver, defina `SE_CHROMEDRIVER` com o caminho de um driver local validado com o Chrome instalado.

```bash
cd "$projeto"
"$python_venv" -B -m pytest tests_ui/ -v -p no:cacheprovider
```

Cada caso recebe cópias próprias dos JSON em `tmp_path` e um Uvicorn com porta dinâmica. As fixtures encerram o servidor e o navegador ao fim do caso. Os nomes são únicos, as datas são calculadas sete dias no futuro e os Page Objects usam esperas explícitas. Chamadas diretas à API preparam as pré-condições. As ações avaliadas e as verificações ocorrem pela interface.

## Relatórios e evidências

A [matriz de casos](tests_ui/casos_de_teste.csv) registra o resultado de CT01 a CT08. O [registro das execuções](../../resultados/projeto-anterior/registro_execucoes.md) reúne os relatórios HTML e XML, versões e ocorrências. Se um teste falhar com o Chrome aberto, o pytest informa o caminho da captura na pasta temporária do caso. As três rodadas oficiais passaram integralmente e não geraram capturas de falha.

## Regras de Negócio Implementadas

- Laboratório não pode ter nome duplicado
- Reserva não pode ser feita para data passada
- Hora de fim deve ser posterior à hora de início
- Laboratório inativo não aceita novas reservas
- Reservas não podem conflitar com reservas já aprovadas no mesmo horário
- Apenas reservas com status **PENDENTE** podem ser avaliadas
- Rejeição exige justificativa obrigatória
- Cancelamento só é permitido pelo próprio solicitante
- Reserva cancelada não bloqueia novos agendamentos

## Histórias de Usuário

| ID | História |
|---|---|
| US01 | Como administrador, desejo gerenciar os laboratórios para manter as informações atualizadas |
| US02 | Como usuário, desejo consultar os laboratórios disponíveis para verificar sua disponibilidade |
| US03 | Como usuário, desejo solicitar uma reserva de laboratório para realizar minhas atividades |
| US04 | Como administrador, desejo aprovar ou rejeitar solicitações de reserva para controlar a utilização |
| US05 | Como solicitante, desejo cancelar uma reserva para liberar o laboratório quando necessário |

## Repositório

[https://github.com/NicolasDamasceno/Sistema-Reserva-Laboratorio](https://github.com/NicolasDamasceno/Sistema-Reserva-Laboratorio)
