import os
from src.pacotes.utils.nomes_arquivos import PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT, PASTA_LOGS

def criar_pastas() -> None:
    """
    Cria todas as pastas necessárias para o processamento. Temp, Input, Output e Logs.
    Para adicionar mais pastas basta passá-las em formato de Path para a variavel lista_pastas.
    """
    lista_pastas = [PASTA_TEMP, PASTA_INPUT, PASTA_OUTPUT, PASTA_LOGS]

    for pasta in lista_pastas:
        os.makedirs(pasta, exist_ok=True)