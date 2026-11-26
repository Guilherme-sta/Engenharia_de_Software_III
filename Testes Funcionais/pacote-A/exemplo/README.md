# Exemplo resolvido A: Fluxo de pedido (Sabor Express)

Cópia da solução do professor (`trabalho2-funcionalidades/solucao-professor/python`).
Ela serve de modelo para o desafio e não é avaliada sozinha.

| Caso | O que verifica |
|---|---|
| CT01 | Pedido completo: total R$ 54.80 (2 × 22,90 + 9,00) no carrinho e na confirmação |
| CT02 | Finalizar sem endereço mostra "Informe um endereço de entrega válido." |
| CT03 | Finalizar sem pagamento mostra "Selecione a forma de pagamento." |
| CT04 | Depois do pedido, o carrinho fica vazio |
| CT05 | Abrir `/carrinho` sem login redireciona para `/login` |

## O que aprendemos com ele (e reaproveitamos no desafio)
- A fixture `carrinho_com_itens` monta uma pré-condição comum e devolve um Page Object pronto.
  No desafio, a fixture equivalente é a `oferta`.
- Em `CardapioPage.adicionar_item`, a espera `staleness_of(botao)` evita clicar num elemento
  da página antiga quando o clique recarrega a página. No desafio, usamos a mesma ideia em
  `entrar()` e `confirmar()`.
- O `conftest.py` salva um print em `evidencias/` quando um teste falha.

## Como rodar e registrar
```bash
cd pacote-A/sistema && python app.py          # terminal 1
cd pacote-A/exemplo                           # terminal 2
pytest -v --html=../../resultados/pacote-A/exemplo.html --self-contained-html
```
Anote o resultado em `../../resultados/pacote-A/registro_execucoes.md`.
