from acessarLattes import extrairDadosLattes
from extracaoDadosCurriculo import extrairDadosCurriculo
from extracaoDadosDiretorio import extrairDadosDiretorio
from extracaoDadosProducao import extrairDadosProducao
from utils import escreverCSV
from deletarArquivos import deletarArquivosTemporarios
import os
from nomes_arquivos_enum import Arquivos
from criarPastas import CriarPastas
from processados import NomeProcessado, AnotarNomeProcessado
import logs

def main(nome: str):
    #Variaveis contendo o caminho da pasta temp e os nomes dos arquivos com as extensões
    temp = Arquivos.PASTA_TEMP.value
    curriculo = Arquivos.CURRICULO.value
    producao = Arquivos.PRODUCAO.value
    csv_erro = Arquivos.ERRO.value
    curriculo = curriculo.split('/')[-1]
    producao = producao.split('/')[-1]

    extrairDadosLattes(nome)
    lista_arquivos = os.listdir(temp)
    if curriculo in lista_arquivos:
        id_lattes = extrairDadosCurriculo()
        extrairDadosDiretorio(id_lattes)
        
        if producao in lista_arquivos:
            extrairDadosProducao(id_lattes)  
            logger.info('Processado com sucesso')      
            AnotarNomeProcessado(nome)    
    else:
        escreverCSV(csv_erro, nome, texto='Não foi possivel baixar o curriculo')
        logger.warning(f'Não foi possivel baixar o curriculo de {nome}')
        AnotarNomeProcessado(nome)


if __name__== "__main__":
    logger = logs.logger
    logger.info('Execução iniciada')
    input_csv = Arquivos.INPUT.value
    
    with open(input_csv) as csv:
        row = csv.readline()
        # while(row):

        for _ in range(100):
            # try:
                nome = csv.readline().strip()
                if not NomeProcessado(nome):
                    logger.info(f'Processando {nome}')
                    deletarArquivosTemporarios()
                    main(nome)
                    
            # except Exception as e:
            #     print(e)
            #     continue