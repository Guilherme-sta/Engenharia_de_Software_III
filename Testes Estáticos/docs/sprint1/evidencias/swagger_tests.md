# Evidências de Testes - Swagger

## Ambiente

* Framework: FastAPI
* Documentação: Swagger UI
* Data dos testes: 21/06/2026

---

## Teste 01 - Listagem de Laboratórios

### Endpoint

GET /laboratorios

### Resultado Esperado

Retornar todos os laboratórios cadastrados.

### Resultado Obtido

HTTP 200 OK

Laboratório retornado:

* Laboratório de Informática
* Capacidade: 30
* Status: ativo

### Evidência

Arquivo: swagger_get_laboratorios.png

### Status

Aprovado.

---

## Teste 02 - Cadastro de Laboratório

### Endpoint

POST /laboratorios

### Resultado Esperado

Cadastrar novo laboratório.

### Resultado Obtido

Laboratório cadastrado com sucesso.

### Evidência

Arquivo: swagger_post_laboratorio.png

### Status

Aprovado.

---

## Teste 03 - Cadastro de Reserva

### Endpoint

POST /reservas

### Resultado Esperado

Registrar nova reserva.

### Resultado Obtido

Reserva registrada com sucesso.

### Evidência

Arquivo: swagger_post_reserva.png

### Status

Aprovado.

---

## Teste 04 - Listagem de Reservas

### Endpoint

GET /reservas

### Resultado Esperado

Retornar reservas cadastradas.

### Resultado Obtido

Lista retornada corretamente.

### Evidência

Arquivo: swagger_get_reservas.png

### Status

Aprovado.

---

## Conclusão

Todos os endpoints implementados na Sprint 01 foram executados através do Swagger UI e responderam conforme esperado.
