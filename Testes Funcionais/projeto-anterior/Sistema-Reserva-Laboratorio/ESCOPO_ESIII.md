# Recorte do projeto anterior — Engenharia de Software III

## Origem e adaptação

O sistema foi importado de `Sistema-Reserva-Laboratorio-main (1).zip`, fornecido pela equipe. A adaptação preserva as regras de negócio da API FastAPI e acrescenta uma interface mínima em `/web/`, com HTML, CSS e JavaScript. Os repositórios continuam a persistir em JSON. A aceitação acadêmica da abordagem permanece a confirmar com o professor.

Foram deixados fora do recorte os documentos e as imagens das sprints anteriores. O `requirements.txt` reúne as dependências usadas nesta entrega. O `requirements-original.txt` é uma referência local do pacote de origem. Os dois testes de cancelamento da suíte HTTP foram ajustados para enviar o solicitante no corpo JSON, de acordo com o contrato da API.

## Fluxos automatizados

| Caso | Fluxo | Comportamento verificado pela interface |
|---|---|---|
| CT01 | Laboratórios | Cadastrar laboratório válido e conferir HTTP 201 e os dados do registro. |
| CT02 | Laboratórios | Rejeitar nome duplicado com HTTP 409, inclusive com diferença entre maiúsculas e minúsculas. |
| CT03 | Laboratórios | Consultar laboratório existente e conferir HTTP 200 e os dados retornados. |
| CT04 | Laboratórios | Consultar ID inexistente e conferir HTTP 404. |
| CT05 | Reservas | Solicitar reserva válida para laboratório ativo em data futura e conferir HTTP 201 e status `pendente`. |
| CT06 | Reservas | Solicitar reserva para laboratório inexistente e conferir HTTP 422 e a mensagem correspondente. |
| CT07 | Reservas | Rejeitar com HTTP 422 a sobreposição com uma reserva aprovada no mesmo laboratório e na mesma data. |
| CT08 | Reservas | Rejeitar com HTTP 422 o cancelamento por outro solicitante e consultar novamente para conferir que a reserva continua pendente. |

Os oito casos usam Selenium, pytest, Page Objects e esperas explícitas. As chamadas HTTP de preparação criam as pré-condições quando necessário. Cada teste Selenium roda com seus próprios JSON temporários e seu próprio servidor. A suíte original usa FastAPI TestClient e sobrescreve os JSON no início de cada caso, por isso o README orienta executá-la em uma cópia isolada.

## Resultados e evidências

Os 14 testes de API passaram em três rodadas históricas. Os oito testes Selenium passaram na execução preliminar e nas três rodadas oficiais. Consulte a [matriz executada](tests_ui/casos_de_teste.csv), o [registro de execuções e ocorrências](../../resultados/projeto-anterior/registro_execucoes.md) e o [README](README.md) para reproduzir os comandos.

Se surgir um defeito, registre o caso, os passos de reprodução, o comportamento esperado, o resultado obtido e a evidência. O registro distingue problemas de ambiente e de preparação dos resultados observados na aplicação.
