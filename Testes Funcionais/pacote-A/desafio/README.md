# Desafio A: Portal de Matrícula Acadêmica

Sistema: `http://localhost:5000/matricula/login` (subir com `python ../sistema/app.py`).
Usuários: `20260001` a `20260200`, senha `senha123`.

## Regras cobertas

| Regra | Comportamento esperado | Casos |
|---|---|---|
| R1 Login | Válido abre a oferta. Inválido: "Matrícula ou senha inválidas." | CT01, CT02a–d |
| R2 Acesso | A oferta só abre após o login | CT03 |
| R3 Quantidade | De 1 a 5. Com 0: "Selecione ao menos uma disciplina." Com 6: "Máximo de 5 disciplinas por semestre." | CT04–CT07 |
| R4 Horário | "Choque de horário entre disciplinas selecionadas." | CT08 |
| R5 Vagas | "Vagas esgotadas: <códigos>." | CT09, CT10 |
| R6 Matrícula única | "Aluno já possui matrícula neste semestre." | CT11, CT13 |
| R7 Sucesso | Mensagem, comprovante COMP-NNNNNN, disciplinas listadas e 1 vaga a menos em cada | CT05, CT06, CT12 |

São **13 casos especificados** em [`casos_de_teste.csv`](casos_de_teste.csv). O mínimo é 10.
Todos estão **automatizados** (16 execuções no pytest, por causa dos parâmetros). O mínimo é 8.

### Técnicas usadas
- **Partição de equivalência:** login válido × inválido (senha errada, matrícula inexistente, campos vazios).
- **Valor-limite:** 0, 1, 5 e 6 disciplinas (R3); aluno `20260201`, logo após o último válido (R1); disciplina com 0 vagas (R5).
- **Tabela de decisão:** R4 (mesmo horário sim/não) e R5 (uma esgotada + uma com vaga → tudo ou nada).

### Testes orientados a dados (`@pytest.mark.parametrize`)
- `test_ct02_login_invalido`: 4 combinações de credenciais inválidas.
- `test_ct04_a_ct07_quantidade_de_disciplinas`: os 4 valores-limite de R3.

## Estrutura do código

```
desafio/
├── conftest.py            fixtures: base_url e driver (abre/fecha o Chrome; print se falhar)
├── apoio_api.py           preparação de dados pela API (reset, ocupar vagas, matrícula prévia)
├── pages/
│   └── matricula_pages.py Page Objects: LoginMatriculaPage, DisciplinasPage, ComprovantePage
├── test_matricula.py      os casos de teste (os asserts ficam aqui)
└── casos_de_teste.csv     matriz de casos
```

Boas práticas exigidas pelo guia e onde cada uma aparece:

| Prática | Onde |
|---|---|
| Localizadores estáveis (`id` / `data-testid`) | Todos os localizadores em `pages/matricula_pages.py`. Nenhum XPath |
| Espera explícita (`WebDriverWait`), sem `sleep` | Toda leitura e clique passa por `self.wait.until(...)` |
| Espera por `staleness_of` após enviar formulário | `entrar()` e `confirmar()`: garante que a leitura seguinte é na página **nova** |
| Page Objects (uma classe por tela) | 3 classes, sem nenhum `assert` dentro delas |
| Testes independentes | Fixture `sistema_zerado` (autouse) chama `POST /api/admin/reset` antes de cada teste |
| Preparar pela API, agir e verificar pela tela | CT09/CT10 lotam MOB pela API; CT11 cria matrícula prévia pela API. A ação e a verificação principal são sempre na tela |
| Provar que a rejeição não gravou nada | Vagas iguais às iniciais **na tela**, e `assert_aluno_sem_matricula` |

## Observações encontradas durante os testes

- **O reset não reinicia a numeração do comprovante.** Depois de `POST /api/admin/reset`,
  o próximo comprovante continua a sequência anterior (ex.: `COMP-000017`), em vez de voltar
  para `COMP-000001`. A regra só exige o formato COMP-NNNNNN, então isso **não é defeito
  de regra**. Mas impede verificar um número exato, por isso o CT12 confere o formato com
  expressão regular.
- **Ordem das validações:** um aluno já matriculado que tente uma disciplina lotada recebe
  "Aluno já possui matrícula" e não "Vagas esgotadas". O guia não define prioridade entre R5
  e R6, então registramos isso só como observação.
- **Verificação da qualidade dos testes:** rodamos a suíte contra uma cópia do sistema com
  dois defeitos propositais: limite de 6 disciplinas e vaga que não é descontada. 4 testes
  falharam (CT07, CT09, CT10, CT12) e cada falha gerou um print em `evidencias/`. Isso mostra
  que os testes detectam esses defeitos.

## Para a apresentação (cada integrante deve saber explicar sem ler)

- **Um caso de teste:** por exemplo, o CT07. Por que 6 é um valor-limite? Porque 5 é o máximo,
  e o primeiro valor inválido é 6. Ele usa 6 disciplinas *sem choque de horário*, para que a
  única regra violada seja a R3.
- **Um localizador:** `[data-testid='disc-MOB'] .vagas`. Ele não depende da posição da linha
  na tabela, então continua funcionando se a ordem das disciplinas mudar.
- **Por que a espera:** depois de clicar em "Confirmar", o navegador troca de página. Sem
  `staleness_of`, o teste poderia ler a mensagem da página antiga ou dar
  `StaleElementReferenceException`. O `sleep` fixo seria lento e ainda assim instável.
