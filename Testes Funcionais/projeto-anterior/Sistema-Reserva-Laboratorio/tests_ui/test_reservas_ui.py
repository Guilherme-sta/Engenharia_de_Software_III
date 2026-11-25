from uuid import uuid4


def test_ct05_solicitar_reserva_valida(reservas_page, laboratorio, dados_reserva):
    dados = dados_reserva(laboratorio["id"])
    status, mensagem = reservas_page.solicitar(**dados)

    assert status == "201"
    assert "Reserva solicitada." in mensagem
    resultado = reservas_page.resultado()
    assert resultado["id"]
    assert resultado == {"id": resultado["id"], **dados, "status": "pendente"}


def test_ct06_rejeitar_laboratorio_inexistente(reservas_page, dados_reserva):
    status, mensagem = reservas_page.solicitar(**dados_reserva(str(uuid4())))

    assert status == "422"
    assert "Laboratório não encontrado." in mensagem


def test_ct07_rejeitar_conflito_de_horario(reservas_page, reserva_aprovada, dados_reserva):
    dados = dados_reserva(reserva_aprovada["laboratorio_id"], hora_inicio="10:00", hora_fim="12:00")
    dados["data"] = reserva_aprovada["data"]
    status, mensagem = reservas_page.solicitar(**dados)

    assert status == "422"
    assert "Já existe reserva aprovada neste horário." in mensagem


def test_ct08_impedir_cancelamento_por_outro_solicitante(reservas_page, reserva_pendente):
    reserva_id = reserva_pendente["id"]
    status, _ = reservas_page.consultar(reserva_id)
    assert status == "200"
    anterior = reservas_page.resultado()
    assert anterior["status"] == "pendente"

    status, mensagem = reservas_page.cancelar(f"Outra pessoa {uuid4().hex}")
    assert status == "422"
    assert "Somente o solicitante pode cancelar a reserva." in mensagem

    status, _ = reservas_page.consultar(reserva_id)
    assert status == "200"
    assert reservas_page.resultado() == anterior
