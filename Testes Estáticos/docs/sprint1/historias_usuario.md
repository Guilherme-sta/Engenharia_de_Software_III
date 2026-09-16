# Histórias de Usuário

## US01 — Gerenciar Laboratórios

**História:**
Como **administrador**, quero **cadastrar e gerenciar laboratórios** para controlar
os espaços disponíveis no IFPI.

**Critérios de Aceitação:**

- CA1: Cadastrar laboratório informando nome (mín. 2 caracteres) e capacidade (> 0).
- CA2: Impedir cadastro de dois laboratórios com o mesmo nome (insensível a maiúsculas).
- CA3: Todo laboratório é criado com status ATIVO por padrão.
- CA4: Editar nome, capacidade e status de um laboratório existente.
- CA5: Inativar laboratório alterando seu status para INATIVO.

**Prioridade:** Alta
**Valor:** Controle centralizado dos laboratórios disponíveis para reserva.

---

## US02 — Consultar Disponibilidade

**História:**
Como **usuário**, quero **consultar a disponibilidade dos laboratórios** para saber
quais estão livres em determinado horário.

**Critérios de Aceitação:**

- CA1: Listar todos os laboratórios com status ATIVO.
- CA2: Verificar disponibilidade de um laboratório informando data, hora de início e hora de fim.
- CA3: Retornar indisponível se houver reserva APROVADA no mesmo laboratório, data e horário conflitante.
- CA4: Retornar indisponível se o laboratório estiver com status INATIVO.

**Prioridade:** Alta
**Valor:** Evitar solicitações desnecessárias e conflitos de agenda.

---

## US03 — Solicitar Reserva

**História:**
Como **usuário**, quero **solicitar a reserva de um laboratório** para garantir
o espaço em uma data e horário específicos.

**Critérios de Aceitação:**

- CA1: Informar laboratório, solicitante, data (YYYY-MM-DD), hora de início e hora de fim (HH:MM).
- CA2: Hora de fim deve ser posterior à hora de início.
- CA3: Não permitir reserva em laboratório com status INATIVO.
- CA4: Não permitir reserva com conflito de horário com reserva já APROVADA no mesmo laboratório e data.
- CA5: Reserva criada com status PENDENTE.

**Prioridade:** Alta
**Valor:** Formalização e rastreabilidade das solicitações de uso dos laboratórios.

---

## US04 — Avaliar Reserva

**História:**
Como **administrador**, quero **aprovar ou rejeitar reservas pendentes** para
controlar o uso dos laboratórios.

**Critérios de Aceitação:**

- CA1: Apenas reservas com status PENDENTE podem ser aprovadas ou rejeitadas.
- CA2: Ao aprovar, verificar se há conflito de horário com outra reserva já APROVADA.
- CA3: Ao rejeitar, exigir justificativa obrigatória.
- CA4: Status da reserva é atualizado para APROVADA ou REJEITADA conforme a ação.

**Prioridade:** Alta
**Valor:** Controle e auditoria do uso dos espaços laboratoriais.

---

## US05 — Cancelar Reserva

**História:**
Como **usuário**, quero **cancelar minha reserva** para liberar o laboratório
caso não precise mais do espaço.

**Critérios de Aceitação:**

- CA1: Somente o solicitante original pode cancelar a reserva.
- CA2: Apenas reservas com status PENDENTE ou APROVADA podem ser canceladas.
- CA3: Status alterado para CANCELADA e data de cancelamento registrada automaticamente.

**Prioridade:** Média
**Valor:** Liberação automática de horários, tornando-os disponíveis para outros usuários.