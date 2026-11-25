# Registro das execuções — Pacote B

## Ambiente

- Sistema operacional: Windows 11
- Python: 3.11.9
- Selenium: 4.52.0
- pytest: 9.2.0
- pytest-html: 4.2.0
- Navegador: Chrome em modo headless
- ChromeDriver: 157.0.8103.78
- Aplicação: http://127.0.0.1:8000

## Exemplo resolvido — Login

| Suíte | Aprovados | Falhas | Tempo |
|---|---|---|---|
| Login válido e inválido | 2/2 | 0 | 8,65 s |

## Desafio B — Inscrições em Minicursos

| Execução | Aprovados | Falhas | Tempo | Relatório |
|---|---|---|---|---|
| 1 (preliminar aproveitada) | 12/12 | 0 | 56,80 s | desafio_execucao1.html |
| 2 | 12/12 | 0 | 57,96 s | desafio_execucao2.html |
| 3 | 12/12 | 0 | 54,26 s | desafio_execucao3.html |

**Tempo médio:** 56,34 segundos.

**Total:** 36 resultados aprovados nas três execuções.

**Oscilações:** nenhuma observada nas três rodadas.

## Observações

Os testes foram executados sequencialmente, utilizando Selenium e pytest.

A API `POST /api/reset` foi utilizada para isolar o estado dos testes.

As verificações principais foram realizadas pela interface web.

Todos os 12 casos de teste passaram nas três execuções, sem falhas ou erros.

Os relatórios HTML e XML foram armazenados em `resultados/pacote-B/`.
