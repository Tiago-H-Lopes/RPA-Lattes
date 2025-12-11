from acessarLattes import extrairDadosLattes
from extracaoDadosCurriculo import extrairDadosCurriculo
from extracaoDadosDiretorio import extrairDadosDiretorio
from extracaoDadosProducao import extrairDadosProducao
from utils import escreverCSV
from deletarArquivos import deletarArquivosTemporarios
import os
from nomes_arquivos_enum import Arquivos
from criarPastas import CriarPastas


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
        dados_curriculo, id_lattes = extrairDadosCurriculo()
        dados_diretorio = extrairDadosDiretorio(id_lattes)
        
        if producao in lista_arquivos:
            dados_producao = extrairDadosProducao(id_lattes)
                
    else:
        escreverCSV(csv_erro, nome, texto='Não foi possivel baixar o curriculo')


if __name__== "__main__":
    CriarPastas()
    input_csv = Arquivos.INPUT.value
    with open(input_csv) as csv:
        row = csv.readline()
        # while(row):
        for _ in range(30):
            try:
                nome = csv.readline().strip()
                print(f'Processando {nome}')
                deletarArquivosTemporarios()
                main(nome)
            except Exception as e:
                print(e)
                continue