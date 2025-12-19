import requests
from bs4 import BeautifulSoup, Tag
from utils import gerarListaDiretorio, escreverCSV
from nomes_arquivos import GRUPOS_PESQUISA, GRUPOS_ATUACAO, LINHA_ATUACAO
from logs import logger

def extrairDadosDiretorio(lattes_id: str) -> None:
    url = f'http://dgp.cnpq.br/dgp/espelhorh/{lattes_id}'
    logger.info(f'Usando método Get na url: {url}')
    response = requests.get(url)
    if(response.status_code==200):
        logger.info(f'URL Acessada com sucesso, inicando extração de dados')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        #Coleta as informações de grupo de pesquisa e retorna uma lista
        groupos_elements: list[Tag] = soup.find_all('div', class_='control-group')
        lista_grupos_pesquisa = []
        titulacao = ''
        for element in groupos_elements:
            try:
                texto: str = element.text.replace('\n', '')
                print(texto)
                if(texto.startswith('Áreas de atuação:')):
                    lista = texto.split('\t')
                    lista_grupos_pesquisa = [item.strip() for item in lista if item.strip()]
                    lista_grupos_pesquisa.pop(0)
                    
                if(texto.startswith('Titulação')):
                    texto = texto.replace('\t', '')
                    valores = texto.split(':')
                    titulacao = valores[1].strip()
                    
            except:
                pass
        
        print(titulacao)
        if lista_grupos_pesquisa:
            escreverCSV(GRUPOS_PESQUISA, lattes_id, lista_grupos_pesquisa)
        
        grupos_pesquisa_elements = soup.find('div', id='gruposPesquisa')
        if grupos_pesquisa_elements:
            rows = grupos_pesquisa_elements.find_all('td', role='gridcell')
            lista_grupos_atuacao = gerarListaDiretorio(rows, 3)
            escreverCSV(GRUPOS_ATUACAO, lattes_id, lista_grupos_atuacao)
                
        linhas = soup.find('div', id='linhasPesquisa')
        if linhas:
            rows = linhas.find_all('td', role='gridcell')
            lista_linhas_atuacao = gerarListaDiretorio(rows, 2)
            escreverCSV(LINHA_ATUACAO, lattes_id, lista_linhas_atuacao)
    else:
        logger.error(f'Não foi possivel acessar a url {url}, status code: {response.status_code}')



if __name__ == '__main__':
    lattes_id=2000279230405792 # SERGIO SAN GREGORIO FAVERO
    lattes_id=3065759072608048 # ALEXANDRE ANDRADE DOS ANJOS JACOME
    extrairDadosDiretorio(lattes_id)