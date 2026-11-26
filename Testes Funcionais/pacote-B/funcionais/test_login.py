from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = 'http://127.0.0.1:8000'

def preencher(driver, senha):
    driver.get(BASE + '/login')
    driver.find_element(By.ID, 'email').send_keys('aluno@ads.local')
    driver.find_element(By.ID, 'senha').send_keys(senha)
    driver.find_element(By.ID, 'entrar').click()

def test_login_valido(driver):
    preencher(driver, 'Teste123!')
    titulo = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'boas-vindas')))
    assert titulo.text == 'Bem-vindo, Aluno ADS'
    assert driver.current_url.endswith('/painel')

def test_login_invalido(driver):
    preencher(driver, 'senha-errada')
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, 'erro'), 'Credenciais inválidas'))
    assert driver.current_url.endswith('/login')
    assert driver.find_elements(By.ID, 'boas-vindas') == []
