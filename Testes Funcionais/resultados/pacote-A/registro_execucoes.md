# Registro das execuções do Pacote A

O guia exige **executar a suíte completa 3 vezes** e registrar se algum teste oscilou
(passou numa rodada e falhou em outra).

Ambiente: Windows 11 (10.0.26200) · Python 3.11.9 · Chrome 157.0.8103.52 · Selenium 4.52.0 · pytest 9.2.0
(ver `../versoes_utilizadas.txt`)

## Exemplo resolvido (fluxo de pedido)

| Execução | Data/hora | Aprovados | Falhos | Relatório |
|---|---|---|---|---|
| Original | 16/11/2026 ~09:52 | 2/5 | 3 (CT01, CT02, CT04) | (saída do terminal) |
| Confirmação pós-ajuste do `conftest.py` | 16/11/2026 ~10:36 | 16/16 | 0 | 166,11 s | desafio_execucao4_pos_ajuste.html |

**O que aconteceu na execução original:** todos os testes que escolhem uma opção na lista
de pagamento (`<select>`) falharam por tempo esgotado (`TimeoutException`). CT03 e CT05,
que não usam a lista, passaram. Causa provável: no Chrome 157 para Windows, o
`Select.select_by_value()` deixa a lista nativa aberta, e o clique seguinte em
"Finalizar pedido" só fecha a lista, sem enviar o formulário.
**Ajuste:** em `CarrinhoPage.finalizar()`, a opção passou a ser escolhida digitando o
nome dela (`send_keys`), e o teste espera a troca de página antes de seguir.

## Desafio A (portal de matrícula)

Comandos (a partir de `pacote-A/desafio`):
```bash
pytest -v --html=../../resultados/pacote-A/desafio_execucao1.html --self-contained-html
pytest -v --html=../../resultados/pacote-A/desafio_execucao2.html --self-contained-html
pytest -v --html=../../resultados/pacote-A/desafio_execucao3.html --self-contained-html
```

| Execução | Data/hora | Aprovados | Falhos | Tempo | Relatório |
|---|---|---|---|---|---|
| Preliminar | 16/11/2026 ~09:55 | 15/16 | 1 (erro) | 152,90 s | (saída do terminal) |
| 1 | 16/11/2026 ~10:00 | 16/16 | 0 | 145,76 s | desafio_execucao1.html |
| 2 | 16/11/2026 ~10:08 | 16/16 | 0 | 154,61 s | desafio_execucao2.html |
| 3 | 16/11/2026 ~10:11 | 16/16 | 0 | 155,65 s | desafio_execucao3.html |

Tempo médio das execuções oficiais: **152,0 s**.

**Algum teste oscilou?** Sim, somente na execução preliminar.
- **Teste:** `test_ct04_a_ct07_quantidade_de_disciplinas[5-disciplinas]`, com erro na
  preparação (login, fixture `oferta`).
- **Erro:** `WebDriverException: unknown error: Node with given id does not belong to the document`.
- **Causa provável:** condição de corrida no ChromeDriver. A espera `EC.staleness_of`
  consultou o botão antigo no instante exato da troca de página e recebeu um erro genérico
  em vez de `StaleElementReferenceException`. Não é defeito do sistema: o mesmo login
  funcionou nos outros 15 testes.
- **Correção:** espera personalizada `pagina_trocou()` em `pages/matricula_pages.py`, que
  também trata esse erro como "a página já trocou". Depois dela, as 3 execuções oficiais
  passaram 16/16, sem oscilação.

## Problemas de ambiente encontrados

| Problema | Sintoma | Solução |
|---|---|---|
| A rede do laboratório bloqueia `googlechromelabs.github.io` | `NoSuchDriverException` com `os error 10060`; os 5 testes do exemplo deram ERROR | O driver foi baixado uma vez e, depois, os testes rodaram com `$env:SE_OFFLINE="true"` |
| Sistema e testes no mesmo terminal | O teste travou esperando o servidor | Sistema no terminal 1 e testes no terminal 2 |

Defeitos encontrados: ver a seção "Observações" em `pacote-A/desafio/README.md`.