# Visão do Produto

## Sistema de Reserva de Laboratórios — IFPI TADS

## Problema

O uso compartilhado de laboratórios em ambientes acadêmicos gera frequentemente
conflitos de horário, sobreposição de reservas e falta de controle sobre a
disponibilidade dos espaços. Sem um sistema formal, professores e monitores
dependem de combinações informais que resultam em ocupações simultâneas,
desperdício de tempo e falta de rastreabilidade.

## Solução

O Sistema de Reserva de Laboratórios é uma API REST desenvolvida em Python com
FastAPI que centraliza e automatiza o processo de reserva dos laboratórios do
IFPI. O sistema permite que usuários solicitem reservas, que administradores
aprovem ou rejeitem essas solicitações, e que o próprio sistema previna conflitos
de horário de forma automática.

## Atores

| Ator            | Descrição                                                        |
|-----------------|------------------------------------------------------------------|
| Administrador   | Responsável por cadastrar laboratórios e avaliar reservas        |
| Usuário         | Professor ou monitor que solicita e cancela reservas             |

## Funcionalidades Principais

- Gerenciar laboratórios (cadastrar, editar, inativar)
- Consultar disponibilidade por data e horário
- Solicitar reservas com validação automática de conflitos
- Aprovar ou rejeitar reservas pendentes
- Cancelar reservas pelo próprio solicitante

## Benefícios Esperados

- Eliminar conflitos de horário entre reservas
- Dar visibilidade sobre quais laboratórios estão disponíveis
- Registrar histórico de uso dos espaços
- Reduzir comunicação informal e erros de agendamento