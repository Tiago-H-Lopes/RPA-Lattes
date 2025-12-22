import logging
from datetime import date
from nomes_arquivos import PASTA_LOGS

now = date.today()
now = date.strftime(now, '%d-%m-%Y')
caminho_log = PASTA_LOGS / f'log {now}.log'
logger = logging.getLogger("RPA")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s")
handler = logging.FileHandler(caminho_log, 'a', encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)