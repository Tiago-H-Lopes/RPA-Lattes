import nomes_arquivos as Arquivos
import os

arquivo_lista_nomes_processados = Arquivos.LISTA_NOMES_PROCESSADOS

def NomeProcessado(nome: str) -> bool:
    lista_nomes_processados = []
    with open(arquivo_lista_nomes_processados, 'r', encoding='utf-8') as arquivo:
        nomes = arquivo.read()
    
    # Quebrar a string em partes usando vírgula
    nomes = nomes.split(", ")

    # Remover as aspas simples extras de cada nome
    lista_nomes_processados = [nome.strip("'") for nome in nomes]
    lista_nomes_processados.pop()
    if(nome in lista_nomes_processados):
        return True
    else:
        return False
    
def AnotarNomeProcessado(nome: str) -> None:
    with open(arquivo_lista_nomes_processados, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'{nome}, ')

if __name__=='__main__':
    lista_nomes = ['ALEXANDRE ANDRADE DOS ANJOS JACOME', 'ALINE FERNANDES DE SA FINTELMAM', 'ANDREA GADELHA NOBREGA LINS', 'BRENO SERIQUE NEVES', 'BRUNA XAVIER REZENDE', 'BRUNO MARCONDES KOZLOWSKI', 'SAYONARA EPIFANIO DOS SANTOS PEREIRA E PEREIRA', 'SERGIO SAN GREGORIO FAVERO', 'TIAGO DALTOE', 'VINICIUS DE LEMOS SILVA']
    # for nome in lista_nomes:
    #     AnotarNomeProcessado(nome)