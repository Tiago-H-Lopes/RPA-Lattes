import os
from nomes_arquivos import PASTA_TEMP

def deletarArquivosTemporarios() -> None:
    temp = PASTA_TEMP
    arquivos = os.listdir(temp)
    for arquivo in arquivos:
        if arquivo.endswith('.html'):
            arquivo = os.path.join(os.curdir, temp, arquivo)
            os.remove(arquivo)