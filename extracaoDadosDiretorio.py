import requests
from bs4 import BeautifulSoup, Tag
from utils import gerarListaDiretorio, escreverCSV
from nomes_arquivos_enum import Arquivos

def extrairDadosDiretorio(lattes_id: str) -> None:
    response = requests.get(f'http://dgp.cnpq.br/dgp/espelhorh/{lattes_id}')
    if(response.status_code==200):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        #Coleta as informações de grupo de pesquisa e retorna uma lista
        groupos_elements: list[Tag] = soup.find_all('div', class_='control-group')
        lista_grupos_pesquisa = []
        for element in groupos_elements:
            try:
                texto: str = element.text.replace('\n', '')
                if(texto.startswith('Áreas de atuação:')):
                    lista = texto.split('\t')
                    lista_grupos_pesquisa = [item.strip() for item in lista if item.strip()]
                    lista_grupos_pesquisa.pop(0)
            except:
                pass

        if lista_grupos_pesquisa:
            escreverCSV(Arquivos.GRUPOS_PESQUISA.value, lattes_id, lista_grupos_pesquisa)
        
        grupos_pesquisa_elements = soup.find('div', id='gruposPesquisa')
        rows = grupos_pesquisa_elements.find_all('td', role='gridcell')
        if rows:
            lista_grupos_atuacao = gerarListaDiretorio(rows, 3)
            escreverCSV(Arquivos.GRUPOS_ATUACAO.value, lattes_id, lista_grupos_atuacao)
                
        linhas = soup.find('div', id='linhasPesquisa')
        rows = linhas.find_all('td', role='gridcell')
        if rows:
            lista_linhas_atuacao = gerarListaDiretorio(rows, 2)
            escreverCSV(Arquivos.LINHA_ATUACAO.value, lattes_id, lista_linhas_atuacao)


if __name__ == '__main__':
    lattes_id=2000279230405792
    extrairDadosDiretorio(lattes_id)