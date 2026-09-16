# Evidências de Teste — Sprint 3

## Resultado do pytest

Todos os testes passaram com sucesso.

## Cobertura dos cenários

| Arquivo                     | Testes | US coberta          |
|-----------------------------|--------|---------------------|
| test_laboratorios.py        | 6      | US01, US02          |
| test_reservas.py            | 8      | US03, US04, US05    |
| **Total**                   | **14** |                     |

## Cenários validados

| US   | Cenário                              | Status  |
|------|--------------------------------------|---------|
| US01 | Cadastrar laboratório válido         | ✅ PASS |
| US01 | Nome duplicado retorna 409           | ✅ PASS |
| US01 | Listar laboratórios                  | ✅ PASS |
| US01 | Buscar por ID existente              | ✅ PASS |
| US01 | Buscar por ID inexistente retorna 404| ✅ PASS |
| US01 | Atualizar laboratório                | ✅ PASS |
| US03 | Solicitar reserva com lab válido     | ✅ PASS |
| US03 | Lab inexistente retorna 422          | ✅ PASS |
| US04 | Aprovar reserva pendente             | ✅ PASS |
| US04 | Rejeitar sem justificativa retorna 422| ✅ PASS |
| US04 | Rejeitar com justificativa           | ✅ PASS |
| US03 | Conflito de horário retorna 422      | ✅ PASS |
| US05 | Cancelar pelo solicitante correto    | ✅ PASS |
| US05 | Cancelar por outro usuário retorna 422| ✅ PASS |