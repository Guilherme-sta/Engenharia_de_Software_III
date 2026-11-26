"""Page Objects do carrinho e da confirmação do pedido.

Ajuste feito pela equipe (Chrome 157 / Windows): o Select.select_by_value()
deixava a lista nativa de pagamento aberta, e o clique seguinte em
"Finalizar pedido" só fechava a lista, sem enviar o formulário (TimeoutException
em CT01, CT02 e CT04). Agora a opção é escolhida digitando o nome dela, e o
teste espera a troca de página após o clique.
"""
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def pagina_trocou(elemento):
    """Igual a EC.staleness_of, mas também aceita o erro genérico do ChromeDriver
    ("Node with given id does not belong to the document") durante a troca de página."""
    def _condicao(_driver):
        try:
            elemento.is_enabled()
            return False
        except (StaleElementReferenceException, WebDriverException):
            return True
    return _condicao


class CarrinhoPage:
    TOTAL = (By.ID, "total")
    ENDERECO = (By.ID, "endereco")
    PAGAMENTO = (By.ID, "pagamento")
    BOTAO_FINALIZAR = (By.ID, "btn-finalizar")
    MENSAGEM_ERRO = (By.ID, "mensagem-erro")
    CARRINHO_VAZIO = (By.ID, "carrinho-vazio")
    LINHAS_ITENS = (By.CSS_SELECTOR, "#tabela-carrinho tr")

    ROTULOS_PAGAMENTO = {"pix": "PIX", "cartao": "Cartão", "dinheiro": "Dinheiro"}

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 5)

    def abrir(self):
        self.driver.get(f"{self.base_url}/carrinho")
        return self

    def total(self):
        return self.wait.until(EC.visibility_of_element_located(self.TOTAL)).text

    def quantidade_de_linhas(self):
        return len(self.driver.find_elements(*self.LINHAS_ITENS)) - 1  # desconta o cabeçalho

    def finalizar(self, endereco="", pagamento=""):
        campo = self.wait.until(EC.visibility_of_element_located(self.ENDERECO))
        campo.clear()
        campo.send_keys(endereco)
        if pagamento:
            lista = self.driver.find_element(*self.PAGAMENTO)
            # Digitar o nome da opção seleciona sem abrir a lista nativa do Chrome
            lista.send_keys(self.ROTULOS_PAGAMENTO[pagamento])
            self.wait.until(lambda d: Select(lista).first_selected_option
                            .get_attribute("value") == pagamento)
        botao = self.driver.find_element(*self.BOTAO_FINALIZAR)
        botao.click()
        self.wait.until(pagina_trocou(botao))  # espera a página nova carregar

    def mensagem_erro(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAGEM_ERRO)).text

    def esta_vazio(self):
        return self.wait.until(EC.visibility_of_element_located(self.CARRINHO_VAZIO)).is_displayed()


class ConfirmacaoPage:
    MENSAGEM_SUCESSO = (By.ID, "mensagem-sucesso")
    TOTAL = (By.ID, "total-pedido")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def mensagem(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAGEM_SUCESSO)).text

    def total(self):
        return self.driver.find_element(*self.TOTAL).text