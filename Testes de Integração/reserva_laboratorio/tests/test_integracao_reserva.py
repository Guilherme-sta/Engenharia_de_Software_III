"""
Testes de Integração — ReservaService + ReservaRepository + LaboratorioRepository
Engenharia de Software III — Trabalho complementar de Teste de Integração

Componentes integrados (todos REAIS, nenhum mock):

    teste -> ReservaService -> ReservaRepository / LaboratorioRepository -> arquivos JSON

No projeto original os repositórios gravam em data/reservas.json e
data/laboratorios.json. Aqui, cada teste aponta os repositórios para arquivos
JSON NOVOS dentro de uma pasta temporária (tmp_path do pytest). Esse é o
equivalente ao banco em memória do exemplo do estoque: a dependência externa é
real, mas isolada, criada do zero a cada teste e descartada no final. Os dados
reais em data/ nunca são tocados.

As asserções leem o resultado DIRETAMENTE do arquivo JSON, sem passar pelo
service nem pelo repositório.
"""
import json

import pytest

from app.exceptions.custom_exceptions import ConflitoDeHorario, OperacaoNaoPermitida
from app.repositories import laboratorio_repo, reserva_repo
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.repositories.reserva_repo import ReservaRepository
from app.schemas.reserva_schema import AvaliarReserva, ReservaCriar
from app.services.reserva_service import ReservaService

LAB_ATIVO = "LAB-ATIVO"
LAB_INATIVO = "LAB-INATIVO"
DATA_FUTURA = "2030-05-20"  # o schema recusa datas passadas


# ---------------------------------------------------------------------------
# Infraestrutura do teste
# ---------------------------------------------------------------------------
@pytest.fixture
def arquivos(tmp_path, monkeypatch):
    """Cria arquivos JSON temporários e faz os repositórios usarem eles."""
    arq_labs = tmp_path / "laboratorios.json"
    arq_reservas = tmp_path / "reservas.json"

    escrever_json(arq_labs, [
        {"id": LAB_ATIVO, "nome": "Lab 1", "capacidade": 20, "status": "ativo"},
        {"id": LAB_INATIVO, "nome": "Lab 2", "capacidade": 15, "status": "inativo"},
    ])
    escrever_json(arq_reservas, [])

    # Os repositórios leem o caminho da constante DATA_FILE do módulo.
    # monkeypatch troca o caminho só durante o teste e desfaz ao final.
    monkeypatch.setattr(laboratorio_repo, "DATA_FILE", arq_labs)
    monkeypatch.setattr(reserva_repo, "DATA_FILE", arq_reservas)

    return {"labs": arq_labs, "reservas": arq_reservas}


@pytest.fixture
def service(arquivos):
    return ReservaService(reserva_repo=ReservaRepository(),
                          lab_repo=LaboratorioRepository())


def escrever_json(caminho, dados):
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def ler_reservas_do_arquivo(arquivos):
    """Lê o arquivo JSON diretamente, sem passar pelo service/repositório."""
    return json.loads(arquivos["reservas"].read_text(encoding="utf-8"))


def reserva_no_arquivo(id, status, inicio, fim, solicitante="Ana"):
    return {
        "id": id, "laboratorio_id": LAB_ATIVO, "solicitante": solicitante,
        "data": DATA_FUTURA, "hora_inicio": inicio, "hora_fim": fim,
        "status": status, "justificativa": None, "data_cancelamento": None,
        "data_hora_solicitacao": "2030-01-01T10:00:00",
    }


# ---------------------------------------------------------------------------
# IT-01 | Caminho feliz: solicitar reserva grava no arquivo como pendente
# ---------------------------------------------------------------------------
def test_solicitar_reserva_grava_no_arquivo_como_pendente(service, arquivos):
    # Act
    retornada = service.solicitar(ReservaCriar(
        laboratorio_id=LAB_ATIVO, solicitante="Guilherme",
        data=DATA_FUTURA, hora_inicio="08:00", hora_fim="10:00"))

    # Assert: lendo o arquivo de volta
    reservas = ler_reservas_do_arquivo(arquivos)
    assert len(reservas) == 1
    gravada = reservas[0]
    assert gravada["id"] == retornada.id and gravada["id"] != ""  # UUID gerado pelo repo
    assert gravada["laboratorio_id"] == LAB_ATIVO
    assert gravada["solicitante"] == "Guilherme"
    assert gravada["hora_inicio"] == "08:00"
    assert gravada["hora_fim"] == "10:00"
    assert gravada["status"] == "pendente"
    assert gravada["data_hora_solicitacao"] is not None  # preenchido pelo repo


# ---------------------------------------------------------------------------
# IT-02 | Caminho feliz: aprovar reserva pendente persiste o novo status
# ---------------------------------------------------------------------------
def test_aprovar_reserva_persiste_status_aprovada(service, arquivos):
    # Arrange
    escrever_json(arquivos["reservas"], [reserva_no_arquivo("R1", "pendente", "08:00", "10:00")])

    # Act
    service.avaliar("R1", AvaliarReserva(acao="aprovar"))

    # Assert
    reservas = ler_reservas_do_arquivo(arquivos)
    assert reservas[0]["status"] == "aprovada"


# ---------------------------------------------------------------------------
# IT-03 | Caminho de ERRO: aprovar com conflito de horário lança exceção
#         e NÃO altera o arquivo (equivalente ao "estoque insuficiente")
# ---------------------------------------------------------------------------
def test_aprovar_com_conflito_lanca_excecao_e_nao_altera_arquivo(service, arquivos):
    # Arrange: R1 já aprovada das 08 às 10; R2 pendente das 09 às 11 (sobrepõe)
    escrever_json(arquivos["reservas"], [
        reserva_no_arquivo("R1", "aprovada", "08:00", "10:00"),
        reserva_no_arquivo("R2", "pendente", "09:00", "11:00", solicitante="Bruno"),
    ])
    conteudo_antes = arquivos["reservas"].read_text(encoding="utf-8")

    # Act + Assert: a exceção é lançada...
    with pytest.raises(ConflitoDeHorario):
        service.avaliar("R2", AvaliarReserva(acao="aprovar"))

    # ...e o arquivo continua exatamente igual (R2 segue pendente)
    assert arquivos["reservas"].read_text(encoding="utf-8") == conteudo_antes
    assert ler_reservas_do_arquivo(arquivos)[1]["status"] == "pendente"


# ---------------------------------------------------------------------------
# IT-04 | Caminho de ERRO: laboratório inativo (lido do arquivo de
#         laboratórios) não aceita reserva e nada é gravado
# ---------------------------------------------------------------------------
def test_solicitar_em_laboratorio_inativo_nao_grava_reserva(service, arquivos):
    with pytest.raises(OperacaoNaoPermitida):
        service.solicitar(ReservaCriar(
            laboratorio_id=LAB_INATIVO, solicitante="Guilherme",
            data=DATA_FUTURA, hora_inicio="08:00", hora_fim="10:00"))

    assert ler_reservas_do_arquivo(arquivos) == []


# ---------------------------------------------------------------------------
# IT-05 | Fluxo completo: o que uma operação grava, a próxima lê.
#         solicitar -> aprovar -> nova solicitação no mesmo horário é barrada
# ---------------------------------------------------------------------------
def test_fluxo_reserva_aprovada_bloqueia_nova_solicitacao_no_mesmo_horario(service, arquivos):
    primeira = service.solicitar(ReservaCriar(
        laboratorio_id=LAB_ATIVO, solicitante="Guilherme",
        data=DATA_FUTURA, hora_inicio="14:00", hora_fim="16:00"))
    service.avaliar(primeira.id, AvaliarReserva(acao="aprovar"))

    with pytest.raises(ConflitoDeHorario):
        service.solicitar(ReservaCriar(
            laboratorio_id=LAB_ATIVO, solicitante="Nicolas",
            data=DATA_FUTURA, hora_inicio="15:00", hora_fim="17:00"))

    reservas = ler_reservas_do_arquivo(arquivos)
    assert len(reservas) == 1  # a segunda não foi gravada
    assert reservas[0]["status"] == "aprovada"
