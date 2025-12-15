import os
from nomes_arquivos import PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT

lista_pastas = [PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT]

for pasta in lista_pastas:
    os.makedirs(pasta, exist_ok=True)