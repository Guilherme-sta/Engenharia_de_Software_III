from enum import Enum

class StatusReserva(str, Enum):
    PENDENTE   = 'pendente'
    APROVADA   = 'aprovada'
    REJEITADA  = 'rejeitada'
    CANCELADA  = 'cancelada'

class Reserva:
    def __init__(self, id: str, laboratorio_id: str, solicitante: str,
                 data: str, hora_inicio: str, hora_fim: str,
                 status: StatusReserva = StatusReserva.PENDENTE,
                 justificativa: str = None, data_cancelamento: str = None,
                 data_hora_solicitacao: str = None):
        self.id = id
        self.laboratorio_id = laboratorio_id
        self.solicitante = solicitante
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status
        self.justificativa = justificativa
        self.data_cancelamento = data_cancelamento
        self.data_hora_solicitacao = data_hora_solicitacao

    def to_dict(self) -> dict:
        return {
            'id': self.id, 'laboratorio_id': self.laboratorio_id,
            'solicitante': self.solicitante, 'data': self.data,
            'hora_inicio': self.hora_inicio, 'hora_fim': self.hora_fim,
            'status': self.status, 'justificativa': self.justificativa,
            'data_cancelamento': self.data_cancelamento,
            'data_hora_solicitacao' : self.data_hora_solicitacao
        }

    @staticmethod
    def from_dict(d: dict) -> 'Reserva':
        return Reserva(id = d['id'], 
                       laboratorio_id = d['laboratorio_id'], 
                       solicitante = d['solicitante'],
                       data = d['data'], 
                       hora_inicio = d['hora_inicio'], 
                       hora_fim = d['hora_fim'],
                       status = StatusReserva(d['status']), 
                       justificativa = d.get('justificativa'),
                       data_cancelamento = d.get('data_cancelamento'),
                       data_hora_solicitacao = d.get('data_hora_solicitacao')
                    )