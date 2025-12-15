import os
from nomes_arquivos import PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT, PASTA_LOGS

lista_pastas = [PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT, PASTA_LOGS]

for pasta in lista_pastas:
    os.makedirs(pasta, exist_ok=True)