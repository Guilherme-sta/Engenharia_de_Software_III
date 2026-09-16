from fastapi import APIRouter, HTTPException, status, Depends
from app.services.laboratorio_service import LaboratorioService
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.schemas.laboratorio_schema import(
    LaboratorioCriar, 
    LaboratorioAtualizar, 
    LaboratorioResposta)

from app.exceptions.custom_exceptions import (
    NomeDuplicado,
    LaboratorioNaoEncontrado)

router = APIRouter(prefix='/laboratorios', tags=['Laboratórios'])
def get_services() -> LaboratorioService:
    return LaboratorioService(LaboratorioRepository())

@router.post('/', response_model=LaboratorioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_laboratorio(dados: LaboratorioCriar,  service : LaboratorioService = Depends(get_services)):
    try:
        lab = service.cadastrar(dados)
        return LaboratorioResposta(**lab.to_dict())
    except NomeDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get('/', response_model=list[LaboratorioResposta])
def listar_laboratorios( service : LaboratorioService = Depends(get_services)):
    labs = service.listar()
    return [LaboratorioResposta(**l.to_dict()) for l in labs]

@router.get('/{id}', response_model=LaboratorioResposta)
def buscar_laboratorio(id: str, service : LaboratorioService = Depends(get_services)):
    try:
        lab = service.buscar(id)
        return LaboratorioResposta(**lab.to_dict())
    except LaboratorioNaoEncontrado as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put('/{id}', response_model=LaboratorioResposta)
def atualizar_laboratorio(
    id: str,
    dados: LaboratorioAtualizar,
    service : LaboratorioService = Depends(get_services)
):
    try:
        lab = service.atualizar(id, dados)
        return LaboratorioResposta(**lab.to_dict())

    except LaboratorioNaoEncontrado as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except NomeDuplicado as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )