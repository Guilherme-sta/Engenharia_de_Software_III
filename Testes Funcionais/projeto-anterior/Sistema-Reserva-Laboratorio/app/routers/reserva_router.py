from fastapi import APIRouter, Depends, HTTPException, status
from app.services.reserva_service import ReservaService
from app.repositories.reserva_repo import ReservaRepository
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.schemas.reserva_schema import CancelarReserva, ReservaCriar, AvaliarReserva, ReservaResposta
from app.exceptions.custom_exceptions import (
    ReservaNaoEncontrada, ConflitoDeHorario,
    OperacaoNaoPermitida, LaboratorioNaoEncontrado)

router = APIRouter(prefix='/reservas', tags=['Reservas'])
def get_service() -> ReservaService:
    return ReservaService(ReservaRepository(), LaboratorioRepository())

@router.post('/', response_model=ReservaResposta, status_code=201)
def solicitar_reserva(dados: ReservaCriar, service: ReservaService = Depends(get_service)):
    try:
        r = service.solicitar(dados)
        return ReservaResposta(**r.to_dict())
    except (ConflitoDeHorario, OperacaoNaoPermitida, LaboratorioNaoEncontrado) as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get('/', response_model=list[ReservaResposta])
def listar_reservas(service: ReservaService = Depends(get_service)):
    return [ReservaResposta(**r.to_dict()) for r in service.listar()]

@router.get('/{id}', response_model=ReservaResposta)
def buscar_reserva(id: str, service: ReservaService = Depends(get_service)):
    try:
        return ReservaResposta(**service.buscar(id).to_dict())
    except ReservaNaoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch('/{id}/avaliar', response_model=ReservaResposta)
def avaliar_reserva(id: str, dados: AvaliarReserva, service: ReservaService = Depends(get_service)):
    try:
        r = service.avaliar(id, dados)
        return ReservaResposta(**r.to_dict())
    except ReservaNaoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ConflitoDeHorario, OperacaoNaoPermitida) as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.patch('/{id}/cancelar', response_model=ReservaResposta)
def cancelar_reserva(id: str, dados: CancelarReserva, service: ReservaService = Depends(get_service)):
    try:
        r = service.cancelar(id, dados.solicitante)
        return ReservaResposta(**r.to_dict())
    except ReservaNaoEncontrada as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OperacaoNaoPermitida as e:
        raise HTTPException(status_code=422, detail=str(e))