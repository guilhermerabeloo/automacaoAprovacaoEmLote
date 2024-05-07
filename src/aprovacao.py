import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import csv
import time
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../log/logsDeExecucao.log'), 
    ]
)

def aprovarNotas(driver):
    wait = WebDriverWait(driver, 20)

    # lendo o arquivo csv
    pasta = 'C:\\Users\\guilherme.rabelo\\Documents\\AutorizacaoEmLoteNf\\config\\zeev.csv'
    try: 
        file = pd.read_csv(pasta, usecols=[0], header=None)
        lista = file[0].to_list()
    except csv.Error as e:
        sys.exit('Erro ao ler o arquivo CSV: {}'.format(e))
    
    # lendo o arquivo json
    with open("../config/config.json", "r", encoding="utf-8") as file:
        sensitive_data = json.load(file)
        sensitive_data = sensitive_data["acessoZeev"]

    mensagemFuro = sensitive_data["mensagemFuro"]

    logging.info(f'Instancias a serem aprovadas: {lista}')
    # aprovando a nota
    for instancia in lista:
        logging.info(f'Aprovando instancia: {instancia}')
        try: 
            # filtrando a instância
            filtro = wait.until(EC.presence_of_element_located((By.ID, 'codflowexecute')))
            filtro.send_keys(instancia)
            filtro.send_keys(Keys.ENTER)

            tarefa = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'prefetch')))
            time.sleep(2)
            tarefa.click()

            # mudando o contexto para o iframe do formulario
            iframeTarefa = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-iframe-show')))
            driver.switch_to.frame(iframeTarefa)
            
            prazoFinanceiroOk = wait.until(EC.presence_of_element_located((By.ID, 'inpatendeAsRegrasFinanceiras'))).get_attribute('value')
            if prazoFinanceiroOk == 'Não' and mensagemFuro == "":
                # fechando o formulario
                driver.switch_to.default_content()
                btnFechar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'close')))
                btnFechar.click()
                logging.warning(f'Instancia #{instancia} nao aprovada por ser furo')
            else: 
                if prazoFinanceiroOk == "Não":
                    driver.execute_script(f"document.getElementById('inpmotivoDoFuro').value = '{mensagemFuro}'")
                # adicionando mensagem padrão de aprovação em lote
                mensagem = wait.until(EC.presence_of_element_located((By.ID, 'inpDsMessage')))
                time.sleep(1)
                mensagem.send_keys('Autorização em lote realizada por RPA')
                time.sleep(1)
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(1)
                btnAdd = driver.find_element(by='id', value='btnAddMessage')
                btnAdd.click()
                time.sleep(3)

                # autorizando
                btnAutorizar = driver.find_element(by='id', value='customBtn_Autorizado')
                btnAutorizar.click()
                
                wait.until(EC.presence_of_element_located((By.ID, 'colorbox')))
                btnFinalizar = driver.find_element(by='css selector', value='.cryo-confirm-dialog .modal-footer button.btn-primary')
                time.sleep(1)
                btnFinalizar.click()
                logging.info(f'Instancia #{instancia} aprovada')

                # saindo do contexto de iframe
                driver.switch_to.default_content()
        except Exception as e:
            logging.info(f'Instancia #{instancia} apresentou erro')
            print(f'Execeção na instancia #{instancia}')
            driver.get('https://fornecedora.zeev.it/my/tasks')

            time.sleep(5)

            continue
        
        # limpando filtro de busca da instância
        wait.until(EC.presence_of_element_located((By.ID, 'codflowexecute')))
        time.sleep(5)

        driver.get('https://fornecedora.zeev.it/my/tasks')
        time.sleep(3)