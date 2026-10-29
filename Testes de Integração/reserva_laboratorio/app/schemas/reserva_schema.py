from pydantic import BaseModel, Field, field_validator
from pydantic import model_validator
from datetime import datetime
from datetime import date
from typing import Optional
from app.models.reserva import StatusReserva

class ReservaCriar(BaseModel):
    laboratorio_id: str
    solicitante: str = Field(..., min_length=2)
    data: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    hora_inicio: str = Field(..., pattern=r'^\d{2}:\d{2}$')
    hora_fim: str = Field(..., pattern=r'^\d{2}:\d{2}$')

    @field_validator("data")
    @classmethod
    def validar_data(cls, valor: str):
        from datetime import date
        data_obj = date.fromisoformat(valor)
        if data_obj < date.today():
            raise ValueError("A reserva não pode ser feita para uma data passada.")
        return valor

    @model_validator(mode="after")
    def validar_horarios(self):

        inicio = datetime.strptime(
            self.hora_inicio,
            "%H:%M"
        )

        fim = datetime.strptime(
            self.hora_fim,
            "%H:%M"
        )

        if inicio >= fim:
            raise ValueError(
                "hora_inicio deve ser menor que hora_fim"
            )

        return self

class AvaliarReserva(BaseModel):
    acao: str = Field(..., pattern='^(aprovar|rejeitar)$')
    justificativa: Optional[str] = None

class ReservaResposta(BaseModel):
    id: str
    laboratorio_id: str
    solicitante: str
    data: str
    hora_inicio: str
    hora_fim: str
    status: StatusReserva
    justificativa: Optional[str] = None
    data_cancelamento: Optional[str] = None
    data_hora_solicitacao: Optional[str] = None

class CancelarReserva(BaseModel):
    solicitante: str = Field(description="Nome do solicitate que deseja cancelar")