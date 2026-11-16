"""Page Objects do portal de Matrícula Acadêmica (Desafio A - Trabalho 2).

Cada classe representa UMA tela e guarda:
  - os localizadores (sempre por id ou data-testid, nunca XPath absoluto);
  - as ações que o usuário faz nela (preencher, marcar, clicar);
  - as leituras do que aparece na tela (mensagens, vagas, comprovante).

Os asserts NÃO ficam aqui: ficam nos testes (test_matricula.py).

Telas:
  /matricula/login        -> LoginMatriculaPage
  /matricula/disciplinas  -> DisciplinasPage
  comprovante (após POST) -> ComprovantePage
"""
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TEMPO_ESPERA = 5  # segundos (espera explícita máxima)


def pagina_trocou(elemento):
    """Condição de espera: o elemento da página antiga não existe mais.

    Faz o mesmo que EC.staleness_of, mas também aceita o erro genérico que o
    ChromeDriver às vezes devolve no meio da troca de página
    ("Node with given id does not belong to the document"). Esse erro também
    significa que a página já trocou.
    """
    def _condicao(_driver):
        try:
            elemento.is_enabled()
            return False                    # ainda é a página antiga
        except (StaleElementReferenceException, WebDriverException):
            return True                     # a página nova já está carregando
    return _condicao


class LoginMatriculaPage:
    CAMPO_MATRICULA = (By.ID, "matricula")
    CAMPO_SENHA = (By.ID, "senha")
    BOTAO_ENTRAR = (By.ID, "btn-entrar")
    MENSAGEM_ERRO = (By.ID, "mensagem-erro")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, TEMPO_ESPERA)

    def abrir(self):
        self.driver.get(f"{self.base_url}/matricula/login")
        self.wait.until(EC.visibility_of_element_located(self.CAMPO_MATRICULA))
        return self

    def entrar(self, matricula, senha):
        campo = self.wait.until(EC.visibility_of_element_located(self.CAMPO_MATRICULA))
        campo.clear()
        campo.send_keys(matricula)
        senha_el = self.driver.find_element(*self.CAMPO_SENHA)
        senha_el.clear()
        senha_el.send_keys(senha)
        botao = self.driver.find_element(*self.BOTAO_ENTRAR)
        botao.click()
        # O clique envia o formulário e carrega OUTRA página (ou a mesma de novo,
        # com o erro). Esperar o botão antigo ficar "stale" garante que a próxima
        # leitura é feita na página nova, e não na velha.
        self.wait.until(pagina_trocou(botao))

    def mensagem_erro(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAGEM_ERRO)).text

    def esta_aberta(self):
        return "/matricula/login" in self.driver.current_url


class DisciplinasPage:
    TABELA = (By.ID, "tabela-disciplinas")
    BOTAO_CONFIRMAR = (By.ID, "btn-confirmar")
    MENSAGEM_ERRO = (By.ID, "mensagem-erro")
    USUARIO_LOGADO = (By.ID, "usuario-logado")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, TEMPO_ESPERA)

    # ---- navegação -------------------------------------------------------
    def abrir(self):
        self.driver.get(f"{self.base_url}/matricula/disciplinas")
        return self

    def esperar_carregar(self):
        self.wait.until(EC.visibility_of_element_located(self.TABELA))
        return self

    def esta_aberta(self):
        """True se a tabela da oferta está na tela (sem esperar: use após a navegação)."""
        return len(self.driver.find_elements(*self.TABELA)) > 0

    # ---- ações -----------------------------------------------------------
    def selecionar(self, *codigos):
        for codigo in codigos:
            caixa = self.wait.until(EC.element_to_be_clickable((By.ID, f"chk-{codigo}")))
            if not caixa.is_selected():
                caixa.click()
        return self

    def confirmar(self):
        botao = self.wait.until(EC.element_to_be_clickable(self.BOTAO_CONFIRMAR))
        botao.click()
        self.wait.until(pagina_trocou(botao)) # a página foi trocada

    def matricular(self, *codigos):
        self.esperar_carregar().selecionar(*codigos).confirmar()

    # ---- leituras --------------------------------------------------------
    def usuario_logado(self):
        return self.driver.find_element(*self.USUARIO_LOGADO).text

    def mensagem_erro(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAGEM_ERRO)).text

    def vagas(self, codigo):
        celula = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f"[data-testid='disc-{codigo}'] .vagas")))
        return int(celula.text)

    def todas_as_vagas(self):
        """Dicionário {codigo: vagas} lido da tabela visível."""
        self.esperar_carregar()
        linhas = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='disc-']")
        resultado = {}
        for linha in linhas:
            codigo = linha.get_attribute("data-testid").removeprefix("disc-")
            resultado[codigo] = int(linha.find_element(By.CSS_SELECTOR, ".vagas").text)
        return resultado


class ComprovantePage:
    MENSAGEM_SUCESSO = (By.ID, "mensagem-sucesso")
    COMPROVANTE = (By.ID, "comprovante")
    DISCIPLINAS = (By.ID, "disciplinas-matriculadas")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TEMPO_ESPERA)

    def mensagem(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAGEM_SUCESSO)).text

    def numero(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMPROVANTE)).text

    def disciplinas(self):
        texto = self.wait.until(EC.visibility_of_element_located(self.DISCIPLINAS)).text
        return [c.strip() for c in texto.split(",") if c.strip()]
