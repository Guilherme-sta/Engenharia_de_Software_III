from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class InscricoesPage:
    NOME = (By.ID, "nome")
    EMAIL = (By.ID, "email")
    CURSO = (By.ID, "curso")
    CONFIRMAR = (By.ID, "confirmar")
    SUCESSO = (By.ID, "sucesso")
    ERRO = (By.ID, "erro")
    LINHAS = (By.CSS_SELECTOR, "#lista > li")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"{base_url}/inscricoes"
        self.espera = WebDriverWait(
            driver, 5, ignored_exceptions=(StaleElementReferenceException,)
        )

    def abrir(self):
        self.driver.get(self.url)
        self.espera.until(EC.visibility_of_element_located(self.NOME))

    def inscrever(self, nome, email, curso):
        for seletor, valor in ((self.NOME, nome), (self.EMAIL, email)):
            campo = self.espera.until(EC.element_to_be_clickable(seletor))
            campo.clear()
            campo.send_keys(valor)
        seletor_curso = self.espera.until(EC.element_to_be_clickable(self.CURSO))
        Select(seletor_curso).select_by_value(str(curso))
        self.espera.until(EC.element_to_be_clickable(self.CONFIRMAR)).click()

    def aguardar_sucesso(self):
        return self.espera.until(EC.visibility_of_element_located(self.SUCESSO)).text

    def aguardar_erro(self):
        return self.espera.until(EC.visibility_of_element_located(self.ERRO)).text

    def aguardar_lista(self, quantidade):
        def lista_completa(driver):
            linhas = driver.find_elements(*self.LINHAS)
            if len(linhas) == quantidade:
                registros = [linha.text.removesuffix("Cancelar").strip() for linha in linhas]
                return (registros,)

        registros, = self.espera.until(
            lista_completa, f"A lista não ficou com {quantidade} inscrições"
        )
        return registros

    def cancelar(self, email):
        for linha in self.driver.find_elements(*self.LINHAS):
            if linha.text.split(" / ")[1] == email:
                inscricao_id = linha.get_dom_attribute("data-id")
                botao = (By.CSS_SELECTOR, f'[data-testid="cancelar-{inscricao_id}"]')
                self.espera.until(EC.element_to_be_clickable(botao)).click()
                return inscricao_id
        raise AssertionError(f"Inscrição para {email} não encontrada na lista")

    def aguardar_remocao(self, inscricao_id):
        linha = (By.CSS_SELECTOR, f'#lista > li[data-id="{inscricao_id}"]')
        self.espera.until(lambda driver: not driver.find_elements(*linha))
