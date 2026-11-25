from uuid import uuid4


def test_ct01_cadastrar_laboratorio_valido(laboratorios_page, nome_laboratorio):
    status, mensagem = laboratorios_page.cadastrar(nome_laboratorio, 24)

    assert status == "201"
    assert "Laboratório cadastrado." in mensagem
    resultado = laboratorios_page.resultado()
    assert resultado["id"]
    assert resultado["nome"] == nome_laboratorio
    assert resultado["capacidade"] == "24"
    assert resultado["status"] == "ativo"


def test_ct02_rejeitar_nome_duplicado(laboratorios_page, laboratorio):
    nome = laboratorio["nome"]
    for duplicado in (nome, nome.upper()):
        status, mensagem = laboratorios_page.cadastrar(duplicado, 30)

        assert status == "409"
        assert f'Laboratório com nome "{duplicado}" já existe.' in mensagem


def test_ct03_consultar_laboratorio_existente(laboratorios_page, laboratorio):
    status, mensagem = laboratorios_page.consultar(laboratorio["id"])

    assert status == "200"
    assert "Laboratório encontrado." in mensagem
    assert laboratorios_page.resultado() == {
        **laboratorio, "capacidade": str(laboratorio["capacidade"]),
    }


def test_ct04_consultar_laboratorio_inexistente(laboratorios_page):
    inexistente = str(uuid4())
    status, mensagem = laboratorios_page.consultar(inexistente)

    assert status == "404"
    assert f"Laboratório {inexistente} não encontrado." in mensagem
