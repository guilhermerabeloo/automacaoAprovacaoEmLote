from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def efetuarLogin(driver): 
    # lendo o arquivo json
    with open("../config/config.json", "r", encoding="utf-8") as file:
        sensitive_data = json.load(file)
        sensitive_data = sensitive_data["acessoZeev"]

    login = sensitive_data["login"]
    senha = sensitive_data["senha"]
    usuario = sensitive_data["usuario"]

    # fazendo login
    driver.get('https://fornecedora.zeev.it/my/user-change')
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)
    iframeLogin = wait.until(EC.presence_of_element_located((By.ID, 'ifrContent')))
    driver.switch_to.frame(iframeLogin)

    driver.find_element(by='id', value='login').send_keys(login)
    driver.find_element(by='id', value='password').send_keys(senha)
    driver.find_element(by='id', value='btnLogin').click()
    driver.switch_to.default_content()

    # personificando pessoa
    elementoShadowDOM = wait.until(EC.presence_of_element_located((By.ID, 'userSearch')))
    buscaPessoaPersonificada = driver.execute_script('return arguments[0].shadowRoot.querySelector("#txtSearchUser")', elementoShadowDOM)
    time.sleep(1)
    buscaPessoaPersonificada.send_keys(usuario)
    buscaPessoaPersonificada.send_keys(Keys.ENTER)
    time.sleep(1)
    pessoaPersonificada = driver.execute_script('return arguments[0].shadowRoot.querySelector("tr.select-user")', elementoShadowDOM)
    pessoaPersonificada.click()

    time.sleep(5)