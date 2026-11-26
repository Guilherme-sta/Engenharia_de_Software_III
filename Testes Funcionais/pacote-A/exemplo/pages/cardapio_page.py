"""Page Object da tela de cardápio da Sabor Express."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.carrinho_page import pagina_trocou


class CardapioPage:
    TITULO = (By.TAG_NAME, "h1")
    QTD_CARRINHO = (By.ID, "qtd-carrinho")
    USUARIO_LOGADO = (By.ID, "usuario-logado")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def esta_aberta(self):
        return self.wait.until(EC.text_to_be_present_in_element(self.TITULO, "Cardápio"))

    def usuario_logado(self):
        return self.driver.find_element(*self.USUARIO_LOGADO).text

    def adicionar_item(self, item_id):
        botao = self.wait.until(EC.element_to_be_clickable((By.ID, f"add-{item_id}")))
        botao.click()
        # O clique recarrega a página. Esperamos o botão antigo "sumir" para não
        # clicar num elemento da página velha (pagina_trocou também trata o erro
        # genérico que o ChromeDriver às vezes devolve durante a troca).
        self.wait.until(pagina_trocou(botao))
        return self

    def quantidade_no_carrinho(self):
        return int(self.wait.until(EC.visibility_of_element_located(self.QTD_CARRINHO)).text)