from datetime import date as Date
from app.repositories.reserva_repo import ReservaRepository
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.models.reserva import Reserva, StatusReserva
from app.models.laboratorio import StatusLaboratorio
from app.schemas.reserva_schema import ReservaCriar, AvaliarReserva
from app.exceptions.custom_exceptions import (
    ReservaNaoEncontrada, ConflitoDeHorario,
    OperacaoNaoPermitida, LaboratorioNaoEncontrado)

class ReservaService:
    def __init__(self, reserva_repo: ReservaRepository, lab_repo: LaboratorioRepository):
        self.reserva_repo = reserva_repo
        self.lab_repo = lab_repo

    def _verificar_conflito(self, lab_id: str, data: str,
                            h_inicio: str, h_fim: str, excluir_id: str = None) -> bool:
        for r in self.reserva_repo.listar_por_laboratorio(lab_id):
            if excluir_id and r.id == excluir_id:
                continue
            if r.status != StatusReserva.APROVADA:
                continue
            if r.data != data:
                continue
            if not (h_fim <= r.hora_inicio or h_inicio >= r.hora_fim):
                return True
        return False

    def solicitar(self, dados: ReservaCriar) -> Reserva:
        lab = self.lab_repo.buscar_por_id(dados.laboratorio_id)
        if not lab:
            raise LaboratorioNaoEncontrado('Laboratório não encontrado.')
        if lab.status != StatusLaboratorio.ATIVO:
            raise OperacaoNaoPermitida('Laboratório inativo não aceita reservas.')
        if self._verificar_conflito(dados.laboratorio_id, dados.data,
                                    dados.hora_inicio, dados.hora_fim):
            raise ConflitoDeHorario('Já existe reserva aprovada neste horário.')
        reserva = Reserva(
            id='', laboratorio_id=dados.laboratorio_id,
            solicitante=dados.solicitante, data=dados.data,
            hora_inicio=dados.hora_inicio, hora_fim=dados.hora_fim)
        return self.reserva_repo.salvar(reserva)

    def avaliar(self, id: str, dados: AvaliarReserva) -> Reserva:
        reserva = self.reserva_repo.buscar_por_id(id)
        if not reserva:
            raise ReservaNaoEncontrada('Reserva não encontrada.')
        if reserva.status != StatusReserva.PENDENTE:
            raise OperacaoNaoPermitida('Apenas reservas pendentes podem ser avaliadas.')
        if dados.acao == 'aprovar':
            if self._verificar_conflito(reserva.laboratorio_id, reserva.data,
                                        reserva.hora_inicio, reserva.hora_fim, id):
                raise ConflitoDeHorario('Conflito com reserva já aprovada.')
            reserva.status = StatusReserva.APROVADA
        else:
            if not dados.justificativa:
                raise OperacaoNaoPermitida('Justificativa obrigatória para rejeição.')
            reserva.status = StatusReserva.REJEITADA
            reserva.justificativa = dados.justificativa
        return self.reserva_repo.atualizar(reserva)

    def cancelar(self, id: str, solicitante: str) -> Reserva:
        reserva = self.reserva_repo.buscar_por_id(id)
        if not reserva:
            raise ReservaNaoEncontrada('Reserva não encontrada.')
        if reserva.solicitante.lower() != solicitante.lower():
            raise OperacaoNaoPermitida('Somente o solicitante pode cancelar a reserva.')
        if reserva.status not in [StatusReserva.PENDENTE, StatusReserva.APROVADA]:
            raise OperacaoNaoPermitida('Reserva não pode ser cancelada.')
        reserva.status = StatusReserva.CANCELADA
        reserva.data_cancelamento = str(Date.today())
        return self.reserva_repo.atualizar(reserva)

    def listar(self) -> list[Reserva]:
        return self.reserva_repo.listar()

    def buscar(self, id: str) -> Reserva:
        r = self.reserva_repo.buscar_por_id(id)
        if not r:
            raise ReservaNaoEncontrada('Reserva não encontrada.')
        return r