# Padrões de Projeto — Sprint 2

## Repository Pattern
**Localização:** `app/repositories/`  
Isola o acesso aos dados (arquivos JSON) do restante da aplicação.
Os services nunca leem ou escrevem arquivos diretamente; delegam ao repositório.

## DTO (Data Transfer Object)
**Localização:** `app/schemas/`  
Os schemas Pydantic (`LaboratorioCriar`, `ReservaCriar`, etc.) atuam como DTOs,
definindo exatamente quais dados entram e saem da API em cada operação.

## Service Layer
**Localização:** `app/services/`  
Concentra toda a lógica de negócio, mantendo os routers responsáveis apenas
pelo transporte HTTP e os repositórios responsáveis apenas pela persistência.

## State (implícito)
**Localização:** `app/models/reserva.py`  
O campo `status` da reserva (`PENDENTE`, `APROVADA`, `REJEITADA`, `CANCELADA`)
representa o padrão State: o comportamento permitido muda conforme o estado atual
(ex: só reservas `PENDENTE` podem ser avaliadas).