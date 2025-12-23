import requests
from bs4 import BeautifulSoup, Tag
from src.pacotes.utils import escrever_csv, logger
from src.pacotes.utils.nomes_arquivos import GRUPOS_PESQUISA, TITULACAO, PASTA_OUTPUT

def extrair_dados_diretorio(lattes_id: str) -> None:
    url = f'http://dgp.cnpq.br/dgp/espelhorh/{lattes_id}'
    logger.info(f'Usando método Get na url: {url}')
    response = requests.get(url)
    if(response.status_code==200):
        logger.info(f'URL Acessada com sucesso, inicando extração de dados')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Coleta as informações de grupo de pesquisa e retorna uma lista
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
        
        # Se tiver extraido a titulação escreve no output, se tiver extraido a lista de grupos de pesquisa escreve em outro output tambem
        if titulacao:
            escrever_csv(TITULACAO, lattes_id, texto=titulacao)
        if lista_grupos_pesquisa:
            escrever_csv(GRUPOS_PESQUISA, lattes_id, lista_grupos_pesquisa)

        # Extrai os dados das tabelas
        elements = soup.select('span > div')
        for element in elements:
            # Extrai os cabeçalhos da tabela
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

            # Extrai os valores da tabela
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

            # Monta o dicionario com o cabecalho e o valor e escreve no documento de output
            contador = 0
            titulo = titulo.replace(' ', '_').upper()
            caminho = PASTA_OUTPUT / f'LATTES_OUTPUT_{titulo}.csv'
            for valor in lista_valores:
                contador = 0 if contador == len(lista_cabecalhos) else contador
                cabecalho = lista_cabecalhos[contador]
                dicionario = {}
                dicionario[cabecalho] = valor
                if valor:
                    escrever_csv(caminho, lattes_id, dicionario=dicionario)
                contador += 1

    else:
        logger.error(f'Não foi possivel acessar a url {url}, status code: {response.status_code}')

if __name__ == '__main__':
    lattes_id=2000279230405792 # SERGIO SAN GREGORIO FAVERO
    lattes_id=3065759072608048 # ALEXANDRE ANDRADE DOS ANJOS JACOME
    lista = []

    for l in lista:
        extrair_dados_diretorio(l)