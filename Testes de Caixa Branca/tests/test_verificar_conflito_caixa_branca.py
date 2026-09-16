"""
Testes de Caixa Branca - ReservaService._verificar_conflito
Engenharia de Software III - Atividade Prática de Testes Estruturais

Cada teste corresponde a um dos 8 caminhos basicos (V(G) = 8)
levantados a partir do Grafo de Fluxo de Controle da funcao.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.services.reserva_service import ReservaService
from app.models.reserva import Reserva, StatusReserva


class FakeReservaRepository:
    """Stub que substitui o acesso a arquivo JSON por uma lista em memoria,
    isolando a regra de negocio testada de qualquer dependencia externa."""

    def __init__(self, reservas):
        self._reservas = reservas

    def listar_por_laboratorio(self, lab_id):
        return [r for r in self._reservas if r.laboratorio_id == lab_id]


def make_reserva(id, status, data, hora_inicio, hora_fim, lab_id="LAB1"):
    return Reserva(
        id=id, laboratorio_id=lab_id, solicitante="fulano",
        data=data, hora_inicio=hora_inicio, hora_fim=hora_fim,
        status=status,
    )


def build_service(reservas):
    fake_repo = FakeReservaRepository(reservas)
    # lab_repo nao e usado por _verificar_conflito, entao None e suficiente
    return ReservaService(reserva_repo=fake_repo, lab_repo=None)


# ---------------------------------------------------------------------
# CT-01 | Caminho 1 (basico): reserva aprovada, mesma data, com
# sobreposicao total de horario -> conflito verdadeiro.
# Caminho: N1-N2-N3-N6-N8-N10-N11-N12-N14
# ---------------------------------------------------------------------
def test_ct01_conflito_com_sobreposicao_total():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-10", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "09:00", "11:00")

    assert resultado is True


# ---------------------------------------------------------------------
# CT-02 | Caminho 2: laboratorio sem nenhuma reserva -> zero iteracoes
# do laco -> sem conflito.
# Caminho: N1-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct02_lista_vazia_sem_conflito():
    service = build_service([])

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "09:00", "11:00")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-03 | Caminho 3: excluir_id informado mas pertence a uma reserva
# diferente da que causa conflito -> reserva conflitante nao e pulada.
# Caminho: N1-N2-N3-N4-N6-N8-N10-N11-N12-N14
# ---------------------------------------------------------------------
def test_ct03_excluir_id_diferente_nao_evita_conflito():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-10", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito(
        "LAB1", "2026-06-10", "09:00", "11:00", excluir_id="R99")

    assert resultado is True


# ---------------------------------------------------------------------
# CT-04 | Caminho 4: excluir_id igual ao id da unica reserva da lista
# -> reserva e ignorada (continue) -> sem conflito.
# Caminho: N1-N2-N3-N4-N5-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct04_excluir_id_igual_ignora_a_propria_reserva():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-10", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito(
        "LAB1", "2026-06-10", "09:00", "11:00", excluir_id="R1")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-05 | Caminho 5: reserva existente com status diferente de
# APROVADA (ex.: pendente) -> ignorada -> sem conflito.
# Caminho: N1-N2-N3-N6-N7-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct05_reserva_pendente_nao_gera_conflito():
    reservas = [make_reserva("R1", StatusReserva.PENDENTE, "2026-06-10", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "09:00", "11:00")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-06 | Caminho 6: reserva aprovada porem em data diferente ->
# ignorada -> sem conflito.
# Caminho: N1-N2-N3-N6-N8-N9-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct06_data_diferente_nao_gera_conflito():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-11", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "09:00", "11:00")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-07 | Caminho 7: mesma data, aprovada, mas o novo horario termina
# antes do horario existente comecar (h_fim <= r.hora_inicio) ->
# primeira condicao do OR verdadeira -> sem sobreposicao.
# Caminho: N1-N2-N3-N6-N8-N10-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct07_novo_horario_termina_antes_do_existente_comecar():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-10", "14:00", "16:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "10:00", "12:00")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-08 | Caminho 8: mesma data, aprovada, primeira condicao do OR
# falsa mas segunda verdadeira (h_inicio >= r.hora_fim) -> novo
# horario comeca depois do existente terminar -> sem sobreposicao.
# Caminho: N1-N2-N3-N6-N8-N10-N11-N2-N13-N14
# ---------------------------------------------------------------------
def test_ct08_novo_horario_comeca_apos_o_existente_terminar():
    reservas = [make_reserva("R1", StatusReserva.APROVADA, "2026-06-10", "08:00", "10:00")]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "10:00", "12:00")

    assert resultado is False


# ---------------------------------------------------------------------
# CT-09 | Teste adicional de cobertura de laco: mais de uma iteracao,
# com a primeira reserva sendo pulada (data diferente) e a segunda
# gerando conflito real. Reforca o criterio "mais de uma iteracao".
# ---------------------------------------------------------------------
def test_ct09_multiplas_reservas_conflito_na_segunda_iteracao():
    reservas = [
        make_reserva("R1", StatusReserva.APROVADA, "2026-06-11", "08:00", "10:00"),
        make_reserva("R2", StatusReserva.APROVADA, "2026-06-10", "09:00", "11:00"),
    ]
    service = build_service(reservas)

    resultado = service._verificar_conflito("LAB1", "2026-06-10", "10:00", "12:00")

    assert resultado is True
