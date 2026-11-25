from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Pagina:
    def __init__(self, navegador):
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, 10)

    @staticmethod
    def seletor(testid):
        return By.CSS_SELECTOR, f'[data-testid="{testid}"]'

    def visivel(self, testid):
        return self.espera.until(EC.visibility_of_element_located(self.seletor(testid)))

    def preencher(self, testid, valor):
        campo = self.visivel(testid)
        campo.clear()
        campo.send_keys(str(valor))

    def enviar(self, botao, feedback):
        botao = self.espera.until(EC.element_to_be_clickable(self.seletor(botao)))
        botao.click()

        def resposta_concluida(navegador):
            elemento = navegador.find_element(*self.seletor(feedback))
            if elemento.get_dom_attribute("data-state") in {"success", "error"}:
                return elemento
            return False

        elemento = self.espera.until(resposta_concluida)
        return elemento.get_dom_attribute("data-http-status"), elemento.text

    def campos_resultado(self, prefixo, *campos):
        return {campo: self.visivel(f"{prefixo}-{campo}").text for campo in campos}
