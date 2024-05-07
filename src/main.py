from login import efetuarLogin
from aprovacao import aprovarNotas
from selenium import webdriver
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../log/logsDeExecucao.log'), 
    ]
)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('executable_path=C:\\Users\\guilherme.rabelo\\Documents\\RPA\\chromedriver.exe')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=chrome_options)

def tratarErro(funcao, mensagem):
    try:
        logging.info(f'INICIANDO FLUXO: "{mensagem}"')
        funcao(driver)
        logging.info(f'FLUXO "{mensagem}" FINALIZADO COM SUCESSO\n')
    except Exception as err:
        logging.critical(f'Erro ao "{mensagem}"')


tratarErro(efetuarLogin, 'efetuar login')
tratarErro(aprovarNotas, 'aprovar notas')