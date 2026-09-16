# Evidências de Testes - Sprint 2

## Ambiente

* Framework: FastAPI
* Documentação: Swagger UI
* Sprint: 2

---

## Teste 01 - Consulta de Laboratório por ID

### Endpoint

GET /laboratorios/{id}

### Resultado

Laboratório retornado corretamente.

### Status

Aprovado.

### Evidência

get_laboratorio_por_id.png

---

## Teste 02 - Atualização de Laboratório

### Endpoint

PUT /laboratorios/{id}

### Resultado

Dados atualizados com sucesso.

### Status

Aprovado.

### Evidência

put_laboratorio.png

---

## Teste 03 - Solicitação de Reserva

### Endpoint

POST /reservas

### Resultado

Reserva criada corretamente.

### Status

Aprovado.

### Evidência

post_reserva.png

---

## Teste 04 - Consulta de Reservas

### Endpoint

GET /reservas

### Resultado

Reservas listadas corretamente.

### Status

Aprovado.

### Evidência

get_reserva.png

---

## Teste 05 - Avaliação de Reserva

### Endpoint

PATCH /reservas/{id}/avaliar

### Resultado

Reserva aprovada/rejeitada corretamente.

### Status

Aprovado.

### Evidência

patch_avaliar_reserva.png

---

## Teste 06 - Cancelamento de Reserva

### Endpoint

PATCH /reservas/{id}/cancelar

### Resultado

Reserva cancelada corretamente.

### Status

Aprovado.

### Evidência

patch_cancelar_reserva.png

---

## Conclusão

Todos os endpoints implementados e validados na Sprint 2 responderam conforme esperado durante os testes realizados via Swagger UI.
