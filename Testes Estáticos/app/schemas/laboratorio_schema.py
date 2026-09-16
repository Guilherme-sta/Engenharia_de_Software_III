from pydantic import BaseModel, Field
from typing import Optional

from app.models.laboratorio import StatusLaboratorio


class LaboratorioCriar(BaseModel):
    nome: str = Field(
        ...,
        min_length=2,
        description="Nome do laboratório"
    )

    capacidade: int = Field(
        ...,
        gt=0,
        description="Capacidade máxima de pessoas"
    )


class LaboratorioAtualizar(BaseModel):
    nome: Optional[str] = Field(
        None,
        min_length=2
    )

    capacidade: Optional[int] = Field(
        None,
        gt=0
    )

    status: Optional[StatusLaboratorio] = None


class LaboratorioResposta(BaseModel):
    id: str
    nome: str
    capacidade: int
    status: StatusLaboratorio