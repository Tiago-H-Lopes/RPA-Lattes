import os
from nomes_arquivos_enum import Arquivos

def CriarPastas() -> None:
    temp = Arquivos.PASTA_TEMP.value
    input = Arquivos.PASTA_INPUT.value
    output = Arquivos.PASTA_OUTPUT.value

    lista_pastas = [temp, input, output]

    for pasta in lista_pastas:
        os.makedirs(pasta, exist_ok=True)