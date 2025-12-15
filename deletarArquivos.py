import os
import nomes_arquivos as Arquivos

def deletarArquivosTemporarios() -> None:
    temp = Arquivos.PASTA_TEMP
    arquivos = os.listdir(temp)
    curriculo = Arquivos.CURRICULO
    producao = Arquivos.PRODUCAO
    curriculo = curriculo.split('/')[-1]
    producao = producao.split('/')[-1]
    remover = [curriculo, producao]
    for arquivo in arquivos:
        if arquivo in remover:
            arquivo = os.path.join(os.curdir, temp, arquivo)
            os.remove(arquivo)