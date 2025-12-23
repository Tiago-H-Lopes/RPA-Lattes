from src.pacotes.utils.nomes_arquivos import LISTA_NOMES_PROCESSADOS
import os
from src.pacotes.utils.logs import logger

arquivo_lista_nomes_processados = LISTA_NOMES_PROCESSADOS

#Cria o documento se ele não existir
if not os.path.exists(arquivo_lista_nomes_processados):
    with open(arquivo_lista_nomes_processados, 'w', encoding='utf-8') as arquivo:
        arquivo.write('')

def nome_processado(nome: str) -> bool:
    """
    Verifica se o nome já foi processado ou não.

    :param nome: Nome a ser verificado
    :type nome: str
    :return: Retorna True se o nome já tiver sido processado, retorna False caso ainda não tenha sido processado
    :rtype: bool
    """
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
            return True
        else:
            return False
        
    logger.debug(f'Finalizando False "NomeProcessado" para o nome {nome}')
    return False
    
def anotar_nome_processado(nome: str) -> None:
    """
    Escreve o nome informado no documento de nomes processados
    
    :param nome: Nome completo do candidato
    :type nome: str
    """

    logger.info(f'Anotando "NomeProcessado" para o nome {nome}')
    with open(arquivo_lista_nomes_processados, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'{nome}, ')

if __name__=='__main__':
    lista_nomes = ['ALEXANDRE ANDRADE DOS ANJOS JACOME', 'ALINE FERNANDES DE SA FINTELMAM', 'ANDREA GADELHA NOBREGA LINS', 'BRENO SERIQUE NEVES', 'BRUNA XAVIER REZENDE', 'BRUNO MARCONDES KOZLOWSKI', 'SAYONARA EPIFANIO DOS SANTOS PEREIRA E PEREIRA', 'SERGIO SAN GREGORIO FAVERO', 'TIAGO DALTOE', 'VINICIUS DE LEMOS SILVA']
    # for nome in lista_nomes:
    #     anotar_nome_processado(nome)