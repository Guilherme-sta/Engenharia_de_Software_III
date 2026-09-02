from enum import Enum

class StatusReserva(str, Enum):
    PENDENTE   = 'pendente'
    APROVADA   = 'aprovada'
    REJEITADA  = 'rejeitada'
    CANCELADA  = 'cancelada'

def verificar_conflito(reservas, excluir_id=None, data=None, h_inicio=None, h_fim=None):
    for r in reservas:
        if excluir_id and r.id == excluir_id:
            continue
        if r.status != StatusReserva.APROVADA:
            continue
        if r.data != data:
            continue
        if not (h_fim <= r.hora_inicio or h_inicio >= r.hora_fim):
            return True
    return False
