from nomes_arquivos import LISTA_NOMES_PROCESSADOS
import os
from logs import logger

arquivo_lista_nomes_processados = LISTA_NOMES_PROCESSADOS

with open(arquivo_lista_nomes_processados, 'w', encoding='utf-8') as arquivo:
    arquivo.write('')

def NomeProcessado(nome: str) -> bool:
    logger.debug(f'Iniciando "NomeProcessado" para o nome {nome}')
    lista_nomes_processados = []
    with open(arquivo_lista_nomes_processados, 'r', encoding='utf-8') as arquivo:
        nomes = arquivo.read()
    
    # Quebrar a string em partes usando vírgula
    if nomes:
        nomes = nomes.split(", ")

        # Remover as aspas simples extras de cada nome
        lista_nomes_processados = [nome.strip("'") for nome in nomes]
        lista_nomes_processados.pop()
        if(nome in lista_nomes_processados):
            logger.debug(f'Finalizando True "NomeProcessado" para o nome {nome}')
            return True
        else:
            logger.debug(f'Finalizando False "NomeProcessado" para o nome {nome}')
            return False
        
    logger.debug(f'Finalizando False "NomeProcessado" para o nome {nome}')
    return False
    
def AnotarNomeProcessado(nome: str) -> None:
    logger.debug(f'Anotando "NomeProcessado" para o nome {nome}')
    with open(arquivo_lista_nomes_processados, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'{nome}, ')

if __name__=='__main__':
    lista_nomes = ['ALEXANDRE ANDRADE DOS ANJOS JACOME', 'ALINE FERNANDES DE SA FINTELMAM', 'ANDREA GADELHA NOBREGA LINS', 'BRENO SERIQUE NEVES', 'BRUNA XAVIER REZENDE', 'BRUNO MARCONDES KOZLOWSKI', 'SAYONARA EPIFANIO DOS SANTOS PEREIRA E PEREIRA', 'SERGIO SAN GREGORIO FAVERO', 'TIAGO DALTOE', 'VINICIUS DE LEMOS SILVA']
    # for nome in lista_nomes:
    #     AnotarNomeProcessado(nome)