# Princípios SOLID — Sprint 2

## S — Single Responsibility Principle
Cada classe tem uma única responsabilidade.  
`LaboratorioService` cuida apenas da lógica de negócio de laboratórios.  
`ReservaService` cuida apenas da lógica de reservas.  
Os repositórios cuidam exclusivamente da persistência em JSON.

## O — Open/Closed Principle
As classes de serviço são abertas para extensão e fechadas para modificação.  
Para adicionar um novo tipo de validação (ex: limite de reservas por usuário),
basta criar um novo método no service sem alterar os existentes.

## L — Liskov Substitution Principle
Os repositórios seguem contratos consistentes: qualquer repositório pode ser
substituído por uma versão alternativa (ex: banco de dados) sem quebrar os services,
pois os services dependem dos métodos `salvar`, `listar`, `buscar_por_id` e `atualizar`.

## I — Interface Segregation Principle
Os schemas são separados por responsabilidade:  
`LaboratorioCriar` e `LaboratorioAtualizar` são schemas distintos, evitando que
o cliente envie campos desnecessários dependendo da operação.

## D — Dependency Inversion Principle
`LaboratorioService` não instancia `LaboratorioRepository` diretamente.  
O repositório é injetado via construtor (`__init__`), invertendo a dependência
e facilitando testes e substituição futura.