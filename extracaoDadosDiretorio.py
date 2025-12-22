import requests
from bs4 import BeautifulSoup, Tag
from utils import gerarListaDiretorio, escreverCSV
from nomes_arquivos import GRUPOS_PESQUISA, GRUPOS_ATUACAO, LINHA_ATUACAO, TITULACAO, PASTA_OUTPUT
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
        
        if titulacao:
            escreverCSV(TITULACAO, lattes_id, texto=titulacao)
        if lista_grupos_pesquisa:
            escreverCSV(GRUPOS_PESQUISA, lattes_id, lista_grupos_pesquisa)

        elements = soup.select('span > div')
        for element in elements:
            id = element.get('id')
            if not id : continue
            if id == 'dadosGerais': continue

            titulo = element.select_one('legend')
            if not titulo: continue

            titulo = titulo.get_text(strip=True)
            cabecalhos = element.select('span')
            lista_cabecalhos = []
            lista_cabecalhos_ignorar = ['IOEPEMC', 'ui-button', 'Ações']
            for cabecalho in cabecalhos:
                texto = cabecalho.text
                if texto == 'Ações': break
                if texto in lista_cabecalhos_ignorar : continue
                if texto:
                    lista_cabecalhos.append(texto)

            valores = element.select('td')
            lista_valores = []
            lista_valores_ignorar = ['Nenhum registro adicionado', 'ui-buttonVisualizar']
            for valor in valores:
                texto = valor.text
                texto = texto.strip()
                if texto.startswith('Visualizar espelho'): continue
                pular = False
                for ignorar in lista_valores_ignorar:
                    if ignorar in texto: 
                        pular = True
                        break

                if pular: continue
                lista_valores.append(texto)

            contador = 0
            titulo = titulo.replace(' ', '_').upper()
            caminho = PASTA_OUTPUT / f'LATTES_OUTPUT_{titulo}.csv'
            for valor in lista_valores:
                contador = 0 if contador == len(lista_cabecalhos) else contador
                cabecalho = lista_cabecalhos[contador]
                dicionario = {}
                dicionario[cabecalho] = valor
                if valor:
                    escreverCSV(caminho, lattes_id, dicionario=dicionario)
                contador += 1

    else:
        logger.error(f'Não foi possivel acessar a url {url}, status code: {response.status_code}')



if __name__ == '__main__':
    lattes_id=2000279230405792 # SERGIO SAN GREGORIO FAVERO
    lattes_id=3065759072608048 # ALEXANDRE ANDRADE DOS ANJOS JACOME
    lista = [
    "2558358124098455",
    "9208985005837277",
    "1272058768233040",
    "3329079748927880",
    "0475167659981163",
    "9978224480666395",
    "2633867419420883",
    "7717444217239525",
    "4827680511742964",
    "7300981629114346",
    "1929897521905456",
    "7581141843974703",
    "6208433886573740",
    "8637319515539535",
    "0602933124301833",
    "2444841881701549",
    "7170570436557463",
    "7686691707525007",
    "2194175558834284",
    "2069769466957361",
    "5330490614722659",
    "6182477842336805",
    "2618349568972136",
    "5204063085335824",
    "3050716643641697",
    "5624554983752801",
    "2381161563121871",
    "5754413873836451",
    "4636891232412658",
    "7587451351635053",
    "3615728985559494"
]

    for l in lista:
        extrairDadosDiretorio(l)