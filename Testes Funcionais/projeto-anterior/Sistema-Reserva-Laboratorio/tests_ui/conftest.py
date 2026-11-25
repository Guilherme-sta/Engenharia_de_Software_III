import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from tests_ui.pages.laboratorios_page import LaboratoriosPage
from tests_ui.pages.reservas_page import ReservasPage

PROJETO = Path(__file__).resolve().parents[1]


@pytest.fixture
def url_api(tmp_path):
    dados = tmp_path / "data"
    dados.mkdir()
    for arquivo in ("laboratorios.json", "reservas.json"):
        shutil.copyfile(PROJETO / "data" / arquivo, dados / arquivo)

    caminho_log = tmp_path / "uvicorn.log"
    with caminho_log.open("wb") as log:
        servidor = subprocess.Popen(
            [
                sys.executable, "-B", "-m", "uvicorn", "app.main:app",
                "--app-dir", str(PROJETO), "--host", "127.0.0.1", "--port", "0",
                "--no-use-colors",
            ],
            cwd=tmp_path,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            def endereco_pronto(processo):
                saida = caminho_log.read_text(encoding="utf-8", errors="replace")
                if processo.poll() is not None:
                    pytest.fail(f"Uvicorn encerrou durante a inicialização:\n{saida}")
                endereco = re.search(r"Uvicorn running on (http://127\.0\.0\.1:\d+)", saida)
                return endereco.group(1) if endereco else False

            yield WebDriverWait(servidor, 15, poll_frequency=0.1).until(
                endereco_pronto, message=f"Uvicorn não iniciou. Log: {caminho_log}",
            )
        finally:
            if servidor.poll() is None:
                servidor.terminate()
                try:
                    servidor.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    servidor.kill()
                    servidor.wait()


@pytest.fixture
def navegador(url_api):
    opcoes = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") != "0":
        opcoes.add_argument("--headless")
    opcoes.add_argument("--window-size=1280,900")

    chrome = webdriver.Chrome(options=opcoes)
    try:
        chrome.set_page_load_timeout(20)
        yield chrome
    finally:
        chrome.quit()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    relatorio = yield
    if relatorio.failed and relatorio.when in {"setup", "call"}:
        navegador = item.funcargs.get("navegador")
        pasta = item.funcargs.get("tmp_path")
        if navegador is not None and pasta is not None:
            screenshot = pasta / f"{item.name}-{relatorio.when}.png"
            try:
                salvo = navegador.save_screenshot(str(screenshot))
                mensagem = str(screenshot) if salvo else "Chrome não salvou a captura."
            except WebDriverException as erro:
                mensagem = f"Falha ao capturar a tela: {erro.msg}"
            relatorio.sections.append(("Screenshot Selenium", mensagem))
    return relatorio


@pytest.fixture
def laboratorios_page(navegador, url_api):
    pagina = LaboratoriosPage(navegador)
    pagina.abrir(url_api)
    return pagina


@pytest.fixture
def reservas_page(navegador, url_api):
    pagina = ReservasPage(navegador)
    pagina.abrir(url_api)
    return pagina


@pytest.fixture
def preparar_api(url_api):
    with httpx.Client(base_url=url_api, timeout=5, trust_env=False) as cliente:
        def enviar(metodo, caminho, dados):
            resposta = cliente.request(metodo, caminho, json=dados)
            resposta.raise_for_status()
            return resposta.json()

        yield enviar


@pytest.fixture
def nome_laboratorio():
    return f"Laboratório {uuid4().hex}"


@pytest.fixture
def laboratorio(preparar_api, nome_laboratorio):
    return preparar_api("POST", "/laboratorios/", {"nome": nome_laboratorio, "capacidade": 24})


@pytest.fixture
def dados_reserva():
    def criar(laboratorio_id, *, hora_inicio="09:00", hora_fim="11:00"):
        return {
            "laboratorio_id": laboratorio_id,
            "solicitante": f"Pessoa {uuid4().hex}",
            "data": (date.today() + timedelta(days=7)).isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
        }

    return criar


@pytest.fixture
def reserva_pendente(preparar_api, laboratorio, dados_reserva):
    return preparar_api("POST", "/reservas/", dados_reserva(laboratorio["id"]))


@pytest.fixture
def reserva_aprovada(preparar_api, reserva_pendente):
    return preparar_api("PATCH", f"/reservas/{reserva_pendente['id']}/avaliar", {"acao": "aprovar"})
