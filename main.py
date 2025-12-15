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
            print('Processado com sucesso')      
            AnotarNomeProcessado(nome)    
    else:
        escreverCSV(csv_erro, nome, texto='Não foi possivel baixar o curriculo')
        AnotarNomeProcessado(nome)


if __name__== "__main__":
    logs.logger.info('Execução iniciada')
    input_csv = Arquivos.INPUT.value
    
    with open(input_csv) as csv:
        row = csv.readline()
        # while(row):

        for _ in range(100):
            # try:
                nome = csv.readline().strip()
                if not NomeProcessado(nome):
                    print(f'Processando {nome}')
                    deletarArquivosTemporarios()
                    main(nome)
                    print()
            # except Exception as e:
            #     print(e)
            #     continue