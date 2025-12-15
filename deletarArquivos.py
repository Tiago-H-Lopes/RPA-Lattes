import os
from nomes_arquivos import PASTA_TEMP, CURRICULO, PRODUCAO

def deletarArquivosTemporarios() -> None:
    temp = PASTA_TEMP
    arquivos = os.listdir(temp)
    curriculo = CURRICULO.name
    producao = PRODUCAO.name
    remover = [curriculo, producao]
    for arquivo in arquivos:
        if arquivo in remover:
            arquivo = os.path.join(os.curdir, temp, arquivo)
            os.remove(arquivo)