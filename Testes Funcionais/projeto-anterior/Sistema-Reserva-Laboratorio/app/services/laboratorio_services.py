from app.repositories.laboratorio_repo import LaboratorioRepository
from app.models.laboratorio import Laboratorio, StatusLaboratorio
from app.schemas.laboratorio_schema import LaboratorioCriar, LaboratorioAtualizar
from app.exceptions.custom_exceptions import LaboratorioNaoEncontrado, NomeDuplicado

class LaboratorioService:
    def __init__(self, repo: LaboratorioRepository):
        self.repo = repo

    def cadastrar(self, dados: LaboratorioCriar) -> Laboratorio:
        if self.repo.buscar_por_nome(dados.nome):
            raise NomeDuplicado(f'Laboratório com nome "{dados.nome}" já existe.')
        lab = Laboratorio(id='', nome=dados.nome, capacidade=dados.capacidade)
        return self.repo.salvar(lab)

    def listar(self) -> list[Laboratorio]:
        return self.repo.listar()

    def listar_ativos(self) -> list[Laboratorio]:
        return [l for l in self.repo.listar() if l.status == StatusLaboratorio.ATIVO]

    def buscar(self, id: str) -> Laboratorio:
        lab = self.repo.buscar_por_id(id)
        if not lab:
            raise LaboratorioNaoEncontrado(f'Laboratório {id} não encontrado.')
        return lab

    def atualizar(self, id: str, dados: LaboratorioAtualizar) -> Laboratorio:
        lab = self.repo.buscar_por_id(id)
        if not lab:
            raise LaboratorioNaoEncontrado(f'Laboratório {id} não encontrado.')
        if dados.nome and dados.nome != lab.nome:
            if self.repo.buscar_por_nome(dados.nome):
                raise NomeDuplicado(f'Nome "{dados.nome}" já existe.')
            lab.nome = dados.nome
        if dados.capacidade:
            lab.capacidade = dados.capacidade
        if dados.status:
            lab.status = dados.status
        return self.repo.atualizar(lab)

    def verificar_disponibilidade(self, id: str, data: str,
                                  hora_inicio: str, hora_fim: str) -> bool:
        lab = self.buscar(id)
        if lab.status != StatusLaboratorio.ATIVO:
            return False
        from app.repositories.reserva_repo import ReservaRepository
        from app.models.reserva import StatusReserva
        reserva_repo = ReservaRepository()
        for r in reserva_repo.listar_por_laboratorio(id):
            if r.status != StatusReserva.APROVADA:
                continue
            if r.data != data:
                continue
            if not (hora_fim <= r.hora_inicio or hora_inicio >= r.hora_fim):
                return False
        return True