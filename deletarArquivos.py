import os
from nomes_arquivos_enum import Arquivos

def deletarArquivosTemporarios() -> None:
    temp = Arquivos.PASTA_TEMP.value
    arquivos = os.listdir(temp)
    curriculo = Arquivos.CURRICULO.value
    producao = Arquivos.PRODUCAO.value
    curriculo = curriculo.split('/')[-1]
    producao = producao.split('/')[-1]
    remover = [curriculo, producao]
    for arquivo in arquivos:
        if arquivo in remover:
            arquivo = os.path.join(os.curdir, temp, arquivo)
            os.remove(arquivo)