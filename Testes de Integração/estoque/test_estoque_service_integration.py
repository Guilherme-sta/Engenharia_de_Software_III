"""
Testes de INTEGRAÇÃO: EstoqueService + ProdutoRepository + banco SQLite real (em memória).

Nada é mockado. O teste chama o service de verdade, que chama o repositório de
verdade, que executa SQL de verdade. As asserções leem o resultado DIRETAMENTE
do banco (SELECT), sem passar pelo service nem pelo repositório.
"""
import sqlite3

import pytest

from estoque_service import EstoqueInsuficienteError, EstoqueService
from produto_repository import ProdutoRepository

SCHEMA = """
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL
);
"""

PRODUTO_ID = 1
ESTOQUE_INICIAL = 10


@pytest.fixture
def conexao():
    # Arrange comum: um banco NOVO em memória para cada teste.
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT INTO produtos (id, nome, quantidade) VALUES (?, ?, ?)",
        (PRODUTO_ID, "Teclado", ESTOQUE_INICIAL),
    )
    conn.commit()
    yield conn
    conn.close()  # isola os testes: o banco some ao fechar a conexão


@pytest.fixture
def service(conexao):
    return EstoqueService(ProdutoRepository(conexao))


def quantidade_no_banco(conexao, produto_id):
    """Consulta o banco diretamente, sem passar pelo service/repositório."""
    linha = conexao.execute(
        "SELECT quantidade FROM produtos WHERE id = ?", (produto_id,)
    ).fetchone()
    return linha[0]


def test_adicionar_estoque_atualiza_banco(conexao, service):
    # Act
    service.adicionar_estoque(PRODUTO_ID, 5)

    # Assert: 10 + 5 = 15 persistido no banco
    assert quantidade_no_banco(conexao, PRODUTO_ID) == 15


def test_vender_produto_com_estoque_suficiente(conexao, service):
    # Act
    service.vender_produto(PRODUTO_ID, 3)

    # Assert: 10 - 3 = 7 persistido no banco
    assert quantidade_no_banco(conexao, PRODUTO_ID) == 7


def test_vender_produto_com_estoque_insuficiente_nao_altera_banco(conexao, service):
    # Act + Assert: a exceção é lançada...
    with pytest.raises(EstoqueInsuficienteError):
        service.vender_produto(PRODUTO_ID, 50)

    # ...e o banco continua exatamente como estava
    assert quantidade_no_banco(conexao, PRODUTO_ID) == ESTOQUE_INICIAL


# ---------------------------------------------------------------------------
# Desafio extra: quantidades inválidas de venda (zero, negativa, maior que o estoque)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "quantidade_invalida, excecao_esperada",
    [
        (0, ValueError),
        (-5, ValueError),
        (ESTOQUE_INICIAL + 1, EstoqueInsuficienteError),
    ],
    ids=["zero", "negativa", "maior_que_estoque"],
)
def test_vender_quantidade_invalida_nao_altera_banco(
    conexao, service, quantidade_invalida, excecao_esperada
):
    with pytest.raises(excecao_esperada):
        service.vender_produto(PRODUTO_ID, quantidade_invalida)

    assert quantidade_no_banco(conexao, PRODUTO_ID) == ESTOQUE_INICIAL
