# Product Backlog

## Histórias de Usuário — Prioridade e Planejamento

| ID   | História                        | Prioridade | Sprint Planejada | Status      |
|------|---------------------------------|------------|------------------|-------------|
| US01 | Gerenciar Laboratórios          | Alta       | Sprint 1         | Em progresso |
| US02 | Consultar Disponibilidade       | Alta       | Sprint 1         | Pendente    |
| US03 | Solicitar Reserva               | Alta       | Sprint 1         | Pendente    |
| US04 | Aprovar ou Rejeitar Reserva     | Alta       | Sprint 2         | Pendente    |
| US05 | Cancelar Reserva                | Média      | Sprint 2         | Pendente    |

## Critério de Priorização

A priorização seguiu a dependência funcional entre as histórias:

- US01 é pré-requisito de todas as demais (sem laboratório, não há reserva).
- US02 e US03 formam o fluxo principal de uso do sistema.
- US04 e US05 complementam o ciclo de vida da reserva.

## Backlog Técnico

| Item                                    | Sprint | Responsável  |
|-----------------------------------------|--------|--------------|
| Configurar estrutura do projeto FastAPI | 1      | Guilherme    |
| Criar modelos de domínio                | 1      | Nicolas      |
| Criar repositórios JSON                 | 1      | Nicolas      |
| Criar schemas Pydantic (DTOs)           | 1      | Marcos       |
| Criar exceções customizadas             | 1      | Guilherme    |
| Criar service de laboratório            | 1      | Guilherme    |
| Criar router de laboratórios            | 1      | Marcos       |
| Criar repositório de reservas           | 2      | Nicolas      |
| Criar schemas de reserva                | 2      | Marcos       |
| Criar service de reservas               | 2      | Guilherme    |
| Criar router de reservas                | 2      | Marcos       |
| Documentar SOLID e padrões de projeto   | 2      | Guilherme       |
| Escrever testes automatizados           | 3      | Nicolas      |
| Relatório final                         | 3      | Marcos       |
