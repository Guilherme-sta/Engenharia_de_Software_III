from enum import Enum


class StatusLaboratorio(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class Laboratorio:
    def __init__(
        self,
        id: str,
        nome: str,
        capacidade: int,
        status: StatusLaboratorio = StatusLaboratorio.ATIVO,
    ):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "status": self.status,
        }

    @staticmethod
    def from_dict(d: dict) -> "Laboratorio":
        return Laboratorio(
            id=d["id"],
            nome=d["nome"],
            capacidade=d["capacidade"],
            status=StatusLaboratorio(d["status"]),
        )