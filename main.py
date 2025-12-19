import os
import criarPastas
import logs
from utils import escreverCSV
from acessarLattes import extrairDadosLattes
from deletarArquivos import deletarArquivosTemporarios
from extracaoDadosProducao import extrairDadosProducao
from extracaoDadosCurriculo import extrairDadosCurriculo
from extracaoDadosDiretorio import extrairDadosDiretorio
from processados import NomeProcessado, AnotarNomeProcessado
from nomes_arquivos import PASTA_TEMP, CURRICULO, PRODUCAO, ERRO, INPUT
from logs import logger

def main(nome: str):
    #Variaveis contendo o caminho da pasta temp e os nomes dos arquivos com as extensões
    temp = PASTA_TEMP
    curriculo = CURRICULO.name
    producao = PRODUCAO.name
    csv_erro = ERRO

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
        logger.warning(f'Não foi possivel acessar o curriculo de {nome}')
        AnotarNomeProcessado(nome)


if __name__== "__main__":
    logger.info('Execução iniciada')
    input_csv = INPUT
    
    with open(input_csv) as csv:
        row = csv.readline()
        # while(row):

        for _ in range(100):
            # try:
                nome = csv.readline().strip()
                if not NomeProcessado(nome):
                    logger.info(f'Processando {nome}')
                    #deletarArquivosTemporarios()
                    main(nome)
                    
            # except Exception as e:
            #     logger.error(e)
            #     continue