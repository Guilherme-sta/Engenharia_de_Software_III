"""
DESAFIO A - Trabalho 2: portal de Matrícula Acadêmica (Selenium + pytest)

Regras (Guia do Aluno, Trabalho 2 > Desafio A):
  R1 Login       R2 Acesso só após login     R3 De 1 a 5 disciplinas
  R4 Horário     R5 Vagas                    R6 Matrícula única
  R7 Sucesso: mensagem, comprovante COMP-NNNNNN, disciplinas listadas, 1 vaga a menos

A matriz completa está em casos_de_teste.csv (CT01 a CT13).

Sistema:   python ../sistema/app.py          (http://localhost:5000)
Executar:  pytest -v --html=../../resultados/pacote-A/execucao1.html --self-contained-html
           (HEADLESS=1 para rodar sem janela)

Oferta (estado após o reset):
  ES3 SEG-19h 40 | BD2 TER-19h 40 | PW2 QUA-19h 35 | RED SEG-19h 30
  IHC QUI-19h 30 | EMP SEX-19h 50 | MOB QUA-21h  5
"""
import re

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import apoio_api as api
from pages.matricula_pages import ComprovantePage, DisciplinasPage, LoginMatriculaPage

ALUNO = "20260001"
SENHA = "senha123"

# Combinações SEM choque de horário (cada disciplina num horário diferente)
CINCO_SEM_CHOQUE = ["ES3", "BD2", "PW2", "IHC", "EMP"]
SEIS_SEM_CHOQUE = CINCO_SEM_CHOQUE + ["MOB"]   # MOB é QUA-21h, PW2 é QUA-19h


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def sistema_zerado(base_url):
    """Antes de CADA teste: vagas restauradas e nenhuma matrícula.
    Isso torna os testes independentes e permite rodá-los em qualquer ordem."""
    api.resetar(base_url)
    yield


@pytest.fixture
def vagas_iniciais(base_url):
    return api.vagas_por_api(base_url)


@pytest.fixture
def oferta(driver, base_url):
    """Pré-condição comum: aluno 20260001 logado, na tela da oferta."""
    LoginMatriculaPage(driver, base_url).abrir().entrar(ALUNO, SENHA)
    return DisciplinasPage(driver, base_url).esperar_carregar()


def assert_aluno_sem_matricula(base_url, aluno=ALUNO):
    """Prova de que a rejeição não gravou nada: se o aluno ainda não tem
    matrícula, uma matrícula válida feita agora é aceita (201).
    (Fica no fim do teste porque altera o estado; o reset do próximo teste limpa.)"""
    status, corpo = api.matricular(base_url, aluno, ["EMP"])
    assert status == 201, f"O aluno ficou com matrícula indevida: {corpo}"


# ---------------------------------------------------------------------------
# R1 - Login
# ---------------------------------------------------------------------------
def test_ct01_login_valido(driver, base_url):
    LoginMatriculaPage(driver, base_url).abrir().entrar(ALUNO, SENHA)

    oferta = DisciplinasPage(driver, base_url).esperar_carregar()
    assert driver.current_url.endswith("/matricula/disciplinas")
    assert oferta.usuario_logado() == ALUNO


@pytest.mark.parametrize("matricula, senha", [
    pytest.param("20260001", "errada", id="senha-errada"),
    pytest.param("20269999", "senha123", id="matricula-inexistente"),
    pytest.param("20260201", "senha123", id="fora-da-faixa"),
    pytest.param("", "", id="campos-vazios"),
])
def test_ct02_login_invalido(driver, base_url, matricula, senha):
    login = LoginMatriculaPage(driver, base_url).abrir()
    login.entrar(matricula, senha)

    assert login.mensagem_erro() == "Matrícula ou senha inválidas."
    assert login.esta_aberta()
    assert not DisciplinasPage(driver, base_url).esta_aberta()


# ---------------------------------------------------------------------------
# R2 - Acesso
# ---------------------------------------------------------------------------
def test_ct03_oferta_exige_login(driver, base_url):
    DisciplinasPage(driver, base_url).abrir()

    WebDriverWait(driver, 5).until(EC.url_contains("/matricula/login"))
    assert driver.current_url.endswith("/matricula/login")
    assert not DisciplinasPage(driver, base_url).esta_aberta()


# ---------------------------------------------------------------------------
# R3 - Quantidade (valores-limite 0, 1, 5 e 6) -> teste orientado a dados
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("disciplinas, erro_esperado", [
    pytest.param([], "Selecione ao menos uma disciplina.", id="0-disciplinas"),
    pytest.param(["ES3"], None, id="1-disciplina"),
    pytest.param(CINCO_SEM_CHOQUE, None, id="5-disciplinas"),
    pytest.param(SEIS_SEM_CHOQUE, "Máximo de 5 disciplinas por semestre.", id="6-disciplinas"),
])
def test_ct04_a_ct07_quantidade_de_disciplinas(driver, base_url, oferta, vagas_iniciais,
                                               disciplinas, erro_esperado):
    oferta.matricular(*disciplinas)

    if erro_esperado is None:                       # 1 e 5: limites válidos
        comprovante = ComprovantePage(driver)
        assert comprovante.mensagem() == "Matrícula realizada com sucesso!"
        assert comprovante.disciplinas() == disciplinas
    else:                                           # 0 e 6: limites inválidos
        assert oferta.mensagem_erro() == erro_esperado
        assert oferta.todas_as_vagas() == vagas_iniciais   # nenhuma vaga descontada
        assert_aluno_sem_matricula(base_url)


# ---------------------------------------------------------------------------
# R4 - Choque de horário
# ---------------------------------------------------------------------------
def test_ct08_choque_de_horario(base_url, oferta, vagas_iniciais):
    oferta.matricular("ES3", "RED")                 # as duas são SEG-19h

    assert oferta.mensagem_erro() == "Choque de horário entre disciplinas selecionadas."
    assert oferta.vagas("ES3") == vagas_iniciais["ES3"]
    assert oferta.vagas("RED") == vagas_iniciais["RED"]
    assert_aluno_sem_matricula(base_url)


# ---------------------------------------------------------------------------
# R5 - Vagas
# ---------------------------------------------------------------------------
def test_ct09_vagas_esgotadas(driver, base_url):
    api.lotar_disciplina(base_url, "MOB")           # pré-condição pela API: 5 outros alunos
    LoginMatriculaPage(driver, base_url).abrir().entrar(ALUNO, SENHA)
    oferta = DisciplinasPage(driver, base_url).esperar_carregar()
    assert oferta.vagas("MOB") == 0

    oferta.matricular("MOB")

    assert oferta.mensagem_erro() == "Vagas esgotadas: MOB."
    assert oferta.vagas("MOB") == 0                 # nunca negativa
    assert_aluno_sem_matricula(base_url)


def test_ct10_vaga_esgotada_nao_desconta_as_outras(driver, base_url):
    api.lotar_disciplina(base_url, "MOB")
    LoginMatriculaPage(driver, base_url).abrir().entrar(ALUNO, SENHA)
    oferta = DisciplinasPage(driver, base_url).esperar_carregar()
    vagas_es3_antes = oferta.vagas("ES3")

    oferta.matricular("MOB", "ES3")

    assert oferta.mensagem_erro() == "Vagas esgotadas: MOB."
    assert oferta.vagas("ES3") == vagas_es3_antes   # tudo ou nada
    assert oferta.vagas("MOB") == 0


# ---------------------------------------------------------------------------
# R6 - Matrícula única
# ---------------------------------------------------------------------------
def test_ct11_matricula_unica_por_semestre(driver, base_url):
    status, _ = api.matricular(base_url, ALUNO, ["ES3"])   # matrícula prévia pela API
    assert status == 201
    LoginMatriculaPage(driver, base_url).abrir().entrar(ALUNO, SENHA)
    oferta = DisciplinasPage(driver, base_url).esperar_carregar()
    vagas_bd2_antes = oferta.vagas("BD2")

    oferta.matricular("BD2")

    assert oferta.mensagem_erro() == "Aluno já possui matrícula neste semestre."
    assert oferta.vagas("BD2") == vagas_bd2_antes


# ---------------------------------------------------------------------------
# R7 - Sucesso
# ---------------------------------------------------------------------------
def test_ct12_sucesso_com_comprovante_e_vagas_descontadas(driver, base_url, oferta,
                                                          vagas_iniciais):
    oferta.matricular("ES3", "BD2")

    comprovante = ComprovantePage(driver)
    assert comprovante.mensagem() == "Matrícula realizada com sucesso!"
    assert re.fullmatch(r"COMP-\d{6}", comprovante.numero())
    assert comprovante.disciplinas() == ["ES3", "BD2"]

    vagas_depois = DisciplinasPage(driver, base_url).abrir().todas_as_vagas()
    esperado = dict(vagas_iniciais, ES3=vagas_iniciais["ES3"] - 1,
                    BD2=vagas_iniciais["BD2"] - 1)
    assert vagas_depois == esperado                 # só ES3 e BD2 mudaram, 1 cada


def test_ct13_segunda_matricula_pela_tela_e_recusada(driver, base_url, oferta):
    oferta.matricular("ES3")
    ComprovantePage(driver).mensagem()              # espera o comprovante

    segunda = DisciplinasPage(driver, base_url).abrir().esperar_carregar()
    segunda.matricular("BD2")

    assert segunda.mensagem_erro() == "Aluno já possui matrícula neste semestre."
