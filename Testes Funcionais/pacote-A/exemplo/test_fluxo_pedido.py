"""
Trabalho Prático 2 - SITUAÇÃO RESOLVIDA PELO PROFESSOR
Fluxo de pedido da lanchonete Sabor Express (Selenium + pytest)

Casos de teste (derivados das regras de negócio - ver roteiro):
  CT01 - Pedido completo com sucesso (total correto + mensagem de confirmação)
  CT02 - Finalizar sem endereço exibe erro
  CT03 - Finalizar sem forma de pagamento exibe erro
  CT04 - Após finalizar, o carrinho fica vazio
  CT05 - Página protegida sem login redireciona para o login

Executar:
    pytest -v --html=relatorio.html     (requer: pip install pytest-html)
    HEADLESS=1 pytest -v
"""
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.cardapio_page import CardapioPage
from pages.carrinho_page import CarrinhoPage, ConfirmacaoPage
from pages.login_page import LoginPage


@pytest.fixture
def carrinho_com_itens(driver, base_url):
    """Pré-condição comum: usuário logado com X-Burger (22,90) x2 e Suco (9,00) x1."""
    LoginPage(driver, base_url).abrir().entrar("aluno", "123456")
    cardapio = CardapioPage(driver)
    cardapio.adicionar_item(1).adicionar_item(1).adicionar_item(5)
    assert cardapio.quantidade_no_carrinho() == 3
    return CarrinhoPage(driver, base_url).abrir()


def test_ct01_pedido_completo_com_sucesso(driver, carrinho_com_itens):
    carrinho = carrinho_com_itens
    assert carrinho.quantidade_de_linhas() == 2
    assert carrinho.total() == "R$ 54.80"           # 2 x 22,90 + 9,00

    carrinho.finalizar(endereco="Rua das Flores, 100", pagamento="pix")

    confirmacao = ConfirmacaoPage(driver)
    assert "confirmado" in confirmacao.mensagem()
    assert confirmacao.total() == "R$ 54.80"


def test_ct02_finalizar_sem_endereco_exibe_erro(carrinho_com_itens):
    carrinho_com_itens.finalizar(endereco="", pagamento="pix")
    assert carrinho_com_itens.mensagem_erro() == "Informe um endereço de entrega válido."


def test_ct03_finalizar_sem_pagamento_exibe_erro(carrinho_com_itens):
    carrinho_com_itens.finalizar(endereco="Rua das Flores, 100")
    assert carrinho_com_itens.mensagem_erro() == "Selecione a forma de pagamento."


def test_ct04_carrinho_fica_vazio_apos_pedido(driver, base_url, carrinho_com_itens):
    carrinho_com_itens.finalizar(endereco="Av. Beira Mar, 500", pagamento="cartao")
    ConfirmacaoPage(driver).mensagem()  # espera a confirmação aparecer
    assert CarrinhoPage(driver, base_url).abrir().esta_vazio()


def test_ct05_pagina_protegida_redireciona_para_login(driver, base_url):
    driver.get(f"{base_url}/carrinho")
    WebDriverWait(driver, 5).until(EC.url_contains("/login"))
    assert driver.current_url.endswith("/login")
