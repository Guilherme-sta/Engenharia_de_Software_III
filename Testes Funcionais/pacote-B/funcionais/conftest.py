from pathlib import Path
import os, re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from apoio_api import post


@pytest.fixture
def base_inscricoes():
    return os.getenv("BASE_URL_INSCRICOES", "http://127.0.0.1:8000").rstrip("/")


@pytest.fixture
def reset_inscricoes(base_inscricoes):
    post(base_inscricoes, "/api/reset", 200)


@pytest.fixture
def lotar_curso(reset_inscricoes, base_inscricoes):
    def preparar(inscricoes):
        for nome, email in inscricoes:
            post(base_inscricoes, "/api/inscricoes", 201, {
                "nome": nome, "email": email, "curso": 1,
            })

    return preparar

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.environ.get('HEADLESS') == '1': options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,900')
    if os.environ.get('CHROME_BINARY'): options.binary_location=os.environ['CHROME_BINARY']
    service = Service(os.environ['CHROMEDRIVER']) if os.environ.get('CHROMEDRIVER') else Service()
    browser = webdriver.Chrome(options=options, service=service)
    yield browser
    browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when=='call' and report.failed and 'driver' in item.funcargs:
        dest=Path('evidencias'); dest.mkdir(exist_ok=True)
        name=re.sub(r'[^a-zA-Z0-9_-]','_',item.nodeid)
        item.funcargs['driver'].save_screenshot(str(dest/(name+'.png')))
