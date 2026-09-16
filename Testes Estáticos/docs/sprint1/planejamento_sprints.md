# Planejamento das Sprints

## Visão Geral

| Sprint   | Duração | Meta Principal                                              |
|----------|---------|-------------------------------------------------------------|
| Sprint 1 | 3 dias  | Estrutura do projeto, artefatos de análise e US01 funcional |
| Sprint 2 | 3 dias  | Implementação completa de US02–US05 e documentação técnica  |
| Sprint 3 | 3 dias  | Revisão, testes automatizados, relatório e apresentação     |

---

## Sprint 1 — Análise, Planejamento e Base Arquitetural

**Meta:** Entregar a estrutura inicial do projeto com pelo menos 1 endpoint funcional,
todos os artefatos de análise e o repositório configurado.

**Dia 1 — Planejamento, Repositório e Estrutura**
- Criar artefatos de análise em docs/sprint1/
- Configurar repositório Git e estrutura de pastas
- Criar app/main.py, exceções customizadas e modelo de domínio (base)

**Dia 2 — Modelos, Repositórios e Primeiro Endpoint**
- Implementar modelos de domínio (Laboratorio e Reserva)
- Implementar repositório JSON para laboratórios
- Criar service de laboratório (cadastrar, listar)
- Criar router com endpoints POST /laboratorios e GET /laboratorios

**Dia 3 — Teste, README e Review**
- Testar endpoints via Swagger
- Escrever README com instruções de execução
- Escrever Sprint Review e Sprint Retrospective

**Entregável:** endpoint POST /laboratorios funcionando com validação de nome duplicado.

---

## Sprint 2 — Implementação das Funcionalidades Centrais

**Meta:** Implementar todas as 5 histórias de usuário, persistência completa,
padrões de projeto e princípios SOLID documentados.

**Dia 1 — Planning Poker e US01/US02 completas**
- Realizar planning poker e registrar em docs/sprint2/planning_poker.md
- Completar US01 (edição e inativação de laboratório)
- Implementar US02 (consulta de disponibilidade)

**Dia 2 — US03, US04 e US05**
- Implementar repositório de reservas
- Implementar schemas de reserva
- Implementar service de reservas com US03, US04 e US05
- Criar router de reservas

**Dia 3 — SOLID, Padrões e Documentação**
- Documentar princípios SOLID aplicados
- Documentar padrões de projeto (Repository, DTO, Service Layer, State)
- Registrar regras de negócio formalmente
- Escrever Sprint Review e Retrospective

---

## Sprint 3 — Finalização, Qualidade e Apresentação

**Meta:** Revisar o código, adicionar evidências de teste, elaborar o relatório
final e preparar a apresentação.

**Dia 1 — Revisão de Código e Testes**
- Revisão de código em par (pair review)
- Escrever testes automatizados com pytest
- Gerar evidências de teste (Swagger + pytest)

**Dia 2 — Relatório Final**
- Elaborar relatório final completo em docs/sprint3/
- Atualizar README com tabela de endpoints e instruções finais

**Dia 3 — Apresentação e Retrospective Final**
- Preparar roteiro e slides da apresentação
- Ensaiar demonstração ao vivo via Swagger
- Escrever Retrospective Final
- Criar tag de release v1.0.0 no Git