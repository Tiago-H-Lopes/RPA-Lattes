import os
from src.pacotes.utils.nomes_arquivos import PASTA_TEMP

def deletar_arquivos_temporarios() -> None:
    """
    Deleta todos os arquivos .html da pasta Temp
    """
    temp = PASTA_TEMP
    arquivos = os.listdir(temp)
    for arquivo in arquivos:
        if arquivo.endswith('.html'):
            arquivo = os.path.join(os.curdir, temp, arquivo)
            os.remove(arquivo)