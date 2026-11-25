# Registro de execuções do Sistema de Reserva de Laboratórios

## Ambiente das rodadas oficiais

Execuções realizadas em 25/11/2026 no Windows, com PowerShell, Python 3.11.9 no ambiente virtual compartilhado, Selenium 4.52.0, pytest 9.2.0 e pytest-html 4.2.0. O Chrome 158.0.8127.37 foi executado em modo headless com o ChromeDriver local 157.0.8103.78, selecionado por `SE_CHROMEDRIVER`. Antes da primeira rodada, uma sessão Selenium abriu uma página de verificação e confirmou as versões em uso.

Cada caso usou um processo Uvicorn em uma porta dinâmica e cópias dos dois JSON em um diretório temporário próprio. As rodadas foram sequenciais, com um `--basetemp` diferente para cada uma. Os hashes SHA-256 dos dois JSON originais e dos seis relatórios da API coincidiram antes e depois.

## Suíte original da API

| Execução | Aprovados | Falhas | Erros | Tempo informado | Tempo do XML | Relatórios |
|---|---:|---:|---:|---:|---:|---|
| 1 | 14/14 | 0 | 0 | 1,67 s | 1,634 s | [HTML](api_execucao1.html) · [XML](api_execucao1.xml) |
| 2 | 14/14 | 0 | 0 | ≈ 1,115 s | 1,115 s | [HTML](api_execucao2.html) · [XML](api_execucao2.xml) |
| 3 | 14/14 | 0 | 0 | 1,34 s | 1,342 s | [HTML](api_execucao3.html) · [XML](api_execucao3.xml) |

Esses resultados são a linha de base da API. Na revisão final foram conferidos os relatórios existentes.

### Ocorrência inicial no cancelamento

1. Criar uma reserva pendente e executar `PATCH /reservas/{id}/cancelar` com `solicitante` na query string, sem corpo JSON.
2. Os testes esperavam HTTP 200 para o próprio solicitante e HTTP 422 com rejeição da regra de negócio para outro solicitante.
3. A requisição sem corpo recebeu HTTP 422 de validação. Isso impediu o cancelamento válido e fez com que o HTTP 422 do cenário negativo pudesse ocorrer antes de a regra de autorização ser avaliada.
4. Os dois testes passaram a enviar `json={"solicitante": "..."}`. A correção alinhou a montagem da requisição ao contrato e preservou o endpoint. Os três relatórios da tabela registram a suíte já com a correção.

## Suíte de interface com Selenium

| Execução | Aprovados | Falhas | Erros | Ignorados | Tempo do console | Relatórios |
|---|---:|---:|---:|---:|---:|---|
| Preliminar | 8/8 | 0 | 0 | 0 | 57,50 s | Saída do pytest registrada na Etapa 3 |
| Oficial 1 | 8/8 | 0 | 0 | 0 | 54,35 s | [HTML](ui_execucao1.html) · [XML](ui_execucao1.xml) |
| Oficial 2 | 8/8 | 0 | 0 | 0 | 55,55 s | [HTML](ui_execucao2.html) · [XML](ui_execucao2.xml) |
| Oficial 3 | 8/8 | 0 | 0 | 0 | 59,03 s | [HTML](ui_execucao3.html) · [XML](ui_execucao3.xml) |

Os três XML oficiais registram aprovação de CT01 a CT08, totalizando 24 aprovações em 24 execuções de caso. Nenhum caso alternou entre aprovação e falha. A diferença entre a rodada oficial mais curta e a mais longa foi de 4,68 s no console. Os tempos registrados nos XML foram 54,352 s, 55,541 s e 59,021 s.

### Evidências e ocorrências

- As rodadas oficiais terminaram com código de saída zero. Como todos os casos passaram, a captura de tela por falha não foi acionada. As evidências das aprovações são os relatórios HTML e XML acima.
- Na tentativa inicial da Etapa 3, o Selenium Manager ficou aguardando a resolução do driver e a consulta ao catálogo externo expirou. A execução preliminar completa e as rodadas oficiais usaram o driver local. A sessão de verificação e as três rodadas oficiais abriram o Chrome normalmente.
- Na preparação da Etapa 4, o PowerShell recusou a passagem dos caminhos ao `Get-FileHash` pelo pipeline. O comando foi ajustado para `-LiteralPath` antes do início das rodadas. Essa ocorrência e a espera pelo driver dizem respeito à preparação do ambiente. Nenhum defeito da aplicação foi observado nos casos executados.
- Na revisão final, o pytest coletou os 14 testes HTTP e os oito Selenium sem executá-los. A coleta emitiu um aviso de depreciação do Starlette sobre o uso de HTTPX pelo `TestClient`.
