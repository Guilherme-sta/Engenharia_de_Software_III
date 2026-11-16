"""
Configuração compartilhada do pytest (fixtures).

O Selenium 4.6+ já baixa o driver correto sozinho (Selenium Manager).
Na rede do laboratório: rodar com $env:SE_OFFLINE="true" após o 1º download.

Variáveis de ambiente opcionais:
    BASE_URL  -> endereço do sistema (padrão http://localhost:5000)
    HEADLESS  -> "1" para rodar sem abrir a janela do navegador
    CI        -> "1" ao rodar em contêiner/pipeline (desliga o sandbox do Chrome)
"""
import os
import pathlib

import pytest
from selenium import webdriver

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def driver(request):
    opcoes = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":
        opcoes.add_argument("--headless=new")
    if os.getenv("CI") == "1":  # contêiner / GitHub Actions
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1280,900")

    # Desliga as janelas do próprio Chrome (salvar senha, "senha vazada", autopreenchimento).
    # Elas roubam o foco do teste: teclas e cliques iam para a janela e não para a página.
    # Causa observada no exemplo, que usa a senha "123456".
    opcoes.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    })
    opcoes.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")

    drv = webdriver.Chrome(options=opcoes)
    drv.implicitly_wait(0)  # usamos esperas EXPLÍCITAS (WebDriverWait)
    yield drv
    # Se o teste falhou, salva um print da tela como evidência
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        pasta = pathlib.Path("evidencias")
        pasta.mkdir(exist_ok=True)
        drv.save_screenshot(str(pasta / f"{request.node.name}.png"))
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda o resultado de cada fase do teste para a fixture 'driver' consultar."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    