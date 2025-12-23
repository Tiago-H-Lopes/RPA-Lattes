import logging
from datetime import date
from src.pacotes.utils.nomes_arquivos import PASTA_LOGS

now = date.today()
now = date.strftime(now, '%d-%m-%Y')
caminho_log = PASTA_LOGS / f'log {now}.log'
logger = logging.getLogger("RPA")

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s")
handler = logging.FileHandler(caminho_log, 'a', encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

fmt_console = logging.Formatter(
        "%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s"
    )
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(fmt_console)
logger.addHandler(ch)
logger.propagate = False
