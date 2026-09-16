# Modelo de Entidades

## Laboratório

Representa um espaço físico que pode ser reservado.

| Campo       | Tipo   | Restrições                         | Descrição                          |
|-------------|--------|------------------------------------|------------------------------------|
| id          | string | UUID gerado automaticamente        | Identificador único do laboratório |
| nome        | string | mínimo 2 caracteres, único         | Nome do laboratório                |
| capacidade  | int    | maior que 0                        | Número máximo de pessoas           |
| status      | enum   | ATIVO ou INATIVO                   | Estado atual do laboratório        |

**Regras:**
- O status inicial é sempre ATIVO.
- O nome não pode se repetir (verificação insensível a maiúsculas).
- Laboratórios com status INATIVO não aceitam novas reservas.

**Exemplo em JSON:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "nome": "Lab de Redes",
  "capacidade": 30,
  "status": "ativo"
}
```

---

## Reserva

Representa a solicitação de uso de um laboratório em um período de tempo.

| Campo              | Tipo   | Restrições                                  | Descrição                              |
|--------------------|--------|---------------------------------------------|----------------------------------------|
| id                 | string | UUID gerado automaticamente                 | Identificador único da reserva         |
| laboratorio_id     | string | deve existir na base de laboratórios        | Referência ao laboratório              |
| solicitante        | string | mínimo 2 caracteres                         | Nome de quem fez a solicitação         |
| data               | string | formato YYYY-MM-DD                          | Data da reserva                        |
| hora_inicio        | string | formato HH:MM                               | Hora de início do uso                  |
| hora_fim           | string | formato HH:MM, posterior à hora_inicio      | Hora de término do uso                 |
| status             | enum   | PENDENTE, APROVADA, REJEITADA, CANCELADA    | Estado atual da reserva                |
| justificativa      | string | obrigatório apenas na rejeição              | Motivo de rejeição (quando aplicável)  |
| data_cancelamento  | string | formato YYYY-MM-DD, preenchido ao cancelar  | Data em que foi cancelada              |

**Regras:**
- O status inicial é sempre PENDENTE.
- Não é permitido conflito de horário com reservas APROVADAS no mesmo laboratório e data.
- Somente reservas PENDENTES podem ser aprovadas ou rejeitadas.
- Somente o solicitante original pode cancelar a reserva.
- Somente reservas PENDENTES ou APROVADAS podem ser canceladas.

**Exemplo em JSON:**
```json
{
  "id": "x1y2z3w4-a1b2-c3d4-e5f6-g7h8i9j0k1l2",
  "laboratorio_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "solicitante": "Guilherme",
  "data": "2025-07-01",
  "hora_inicio": "08:00",
  "hora_fim": "10:00",
  "status": "pendente",
  "justificativa": null,
  "data_cancelamento": null
}
```

---

## Relacionamento

```
Laboratorio 1 ──< Reserva N
```

Um laboratório pode ter muitas reservas. Cada reserva pertence a exatamente
um laboratório. O relacionamento é mantido pelo campo `laboratorio_id` na reserva.