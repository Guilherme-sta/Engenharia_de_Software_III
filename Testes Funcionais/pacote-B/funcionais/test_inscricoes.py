import pytest

from pages.inscricoes_page import InscricoesPage


SUCESSO = "Inscrição realizada"
ERRO_NOME = "Nome deve ter de 3 a 60 caracteres"


@pytest.fixture
def pagina(reset_inscricoes, driver, base_inscricoes):
    return InscricoesPage(driver, base_inscricoes)


def test_ct01(pagina):
    pagina.abrir()
    assert pagina.aguardar_lista(0) == []
    pagina.inscrever("Ana Lima", "ana01@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert pagina.aguardar_lista(1) == ["Ana Lima / ana01@example.com / curso 1"]


def test_ct02(pagina):
    pagina.abrir()
    pagina.inscrever("Bruno Silva", "bruno@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert pagina.aguardar_lista(1) == ["Bruno Silva / bruno@example.com / curso 1"]

    pagina.inscrever("Bruno Silva", "bruno@example.com", 2)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert sorted(pagina.aguardar_lista(2)) == [
        "Bruno Silva / bruno@example.com / curso 1",
        "Bruno Silva / bruno@example.com / curso 2",
    ]


def test_ct03(pagina):
    pagina.abrir()
    pagina.inscrever("", "clara@example.com", 1)
    assert pagina.aguardar_erro() == ERRO_NOME
    assert pagina.aguardar_lista(0) == []


def test_ct04(pagina):
    pagina.abrir()
    pagina.inscrever("Diego Lima", "diego@dominio", 1)
    assert pagina.aguardar_erro() == "E-mail inválido"
    assert pagina.aguardar_lista(0) == []


def test_ct05(pagina):
    pagina.abrir()
    pagina.inscrever("Elisa Souza", "elisa@example.com", "")
    assert pagina.aguardar_erro() == "Curso obrigatório"
    assert pagina.aguardar_lista(0) == []


def test_ct06(pagina):
    pagina.abrir()
    pagina.inscrever("Al", "limite02@example.com", 1)
    assert pagina.aguardar_erro() == ERRO_NOME
    assert pagina.aguardar_lista(0) == []


def test_ct07(pagina):
    pagina.abrir()
    pagina.inscrever("Ana", "limite03@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert pagina.aguardar_lista(1) == ["Ana / limite03@example.com / curso 1"]


def test_ct08(pagina):
    nome = "A" * 60
    pagina.abrir()
    pagina.inscrever(nome, "limite60@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert pagina.aguardar_lista(1) == [f"{nome} / limite60@example.com / curso 1"]


def test_ct09(pagina):
    pagina.abrir()
    pagina.inscrever("A" * 61, "limite61@example.com", 1)
    assert pagina.aguardar_erro() == ERRO_NOME
    assert pagina.aguardar_lista(0) == []


def test_ct10(pagina):
    pagina.abrir()
    pagina.inscrever("Fabio Costa", "fabio@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    esperado = ["Fabio Costa / fabio@example.com / curso 1"]
    assert pagina.aguardar_lista(1) == esperado

    pagina.inscrever("Fabio Costa", "  FABIO@EXAMPLE.COM  ", 1)
    assert pagina.aguardar_erro() == "Inscrição já existente"
    assert pagina.aguardar_lista(1) == esperado


def test_ct11(pagina, lotar_curso):
    lotar_curso([("Gina Lima", "gina1@example.com"), ("Gina Souza", "gina2@example.com")])
    pagina.abrir()
    esperado = [
        "Gina Lima / gina1@example.com / curso 1",
        "Gina Souza / gina2@example.com / curso 1",
    ]
    assert sorted(pagina.aguardar_lista(2)) == esperado

    pagina.inscrever("Hugo Dias", "hugo3@example.com", 1)
    assert pagina.aguardar_erro() == "Curso sem vagas"
    assert sorted(pagina.aguardar_lista(2)) == esperado


def test_ct12(pagina, lotar_curso):
    lotar_curso([("Iris Lima", "iris1@example.com"), ("Iris Souza", "iris2@example.com")])
    pagina.abrir()
    remanescente = "Iris Souza / iris2@example.com / curso 1"
    assert sorted(pagina.aguardar_lista(2)) == [
        "Iris Lima / iris1@example.com / curso 1",
        remanescente,
    ]

    inscricao_id = pagina.cancelar("iris1@example.com")
    assert pagina.aguardar_sucesso() == "Inscrição cancelada"
    pagina.aguardar_remocao(inscricao_id)
    assert pagina.aguardar_lista(1) == [remanescente]

    pagina.inscrever("Julia Reis", "julia3@example.com", 1)
    assert pagina.aguardar_sucesso() == SUCESSO
    assert sorted(pagina.aguardar_lista(2)) == [
        remanescente,
        "Julia Reis / julia3@example.com / curso 1",
    ]
