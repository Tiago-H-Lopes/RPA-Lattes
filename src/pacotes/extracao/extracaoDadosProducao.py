import re
from bs4 import BeautifulSoup, Tag
from src.pacotes.utils import  escrever_csv, logger
import src.pacotes.utils.nomes_arquivos as Arquivos

#Funcao Principal
def extrair_dados_producao(id_lattes: int | str, nome: str) -> None:
    """
    Extrai os dados do documento .html contendo os elmentos dos graficos do candidato
    
    :param id_lattes: id_lattes do candido para preenchimento no arquivo de output .csv
    :type id_lattes: int | str
    :param nome: Nome completo do candidato
    :type nome: str
    """

    logger.info(f'Extraindo dado producao - {nome}')

    producao_nome = Arquivos.PRODUCAO.name.replace('{nome}', nome)
    producao = Arquivos.PRODUCAO.with_name(producao_nome)
    with open(producao, encoding='utf-8') as document:
        html = document.read()

    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('div', class_='grafico')

    if elements:
        lista_prod_bibliograficas = gerar_lista_producao(elements, 'Produção Bibliográfica')
        lista_prod_tecnica = gerar_lista_producao(elements, 'Produção Técnica')
        lista_orientacoes = gerar_lista_producao(elements, 'Orientações Concluídas')
        lista_todas_prod = gerar_lista_producao(elements, 'Todas as Produções')
        lista_artigos = gerar_lista_producao_artigos(elements, 'Total de Artigos Publicados por Periódico', soup)

    if lista_prod_bibliograficas:
        escrever_csv(Arquivos.PRODUCOES_BIBLIOGRAFICAS, id_lattes, lista_prod_bibliograficas)

    if lista_prod_tecnica:
        escrever_csv(Arquivos.PRODUCOES_TECNICAS, id_lattes, lista_prod_tecnica)

    if lista_orientacoes:
        escrever_csv(Arquivos.ORIENTACOES, id_lattes, lista_orientacoes)

    if lista_todas_prod:
        escrever_csv(Arquivos.TODAS_PRODUCOES, id_lattes, lista_todas_prod)
        
    if lista_artigos:
        escrever_csv(Arquivos.ARTIGOS_PRODUCAO, id_lattes, lista_artigos)


#Funcoes Auxiliares
def pegar_elementos_producao(elements: Tag, titulo_procurado: str) -> Tag:
    """
    Docstring for pegar_elementos_producao
    
    :param elements: Tag contendo os elementos para serem iterados
    :type elements: Tag
    :param titulo_procurado: Titulo procurado para retornar os elementos
    :type titulo_procurado: str
    :return: Retorna uma Tag contendo os elementos do titulo informado
    :rtype: Tag
    """

    for element in elements:
        titulo: str = element.select_one('h2').text
        titulo = titulo.strip()

        if(titulo==titulo_procurado and titulo_procurado=='Total de Artigos Publicados por Periódico'):
            return element.select_one('div.layout-cell.layout-cell-12')
        
        if(titulo==titulo_procurado):
            return element.select_one('tbody')

def gerar_lista_producao(elements: Tag, titulo_procurado: str) -> list[str]:
    """
    Gera uma lista com todos os valores extraidos para o titulo informado
    
    :param elements: Tag contendo os elementos para serem iterados
    :type elements: Tag
    :param titulo_procurado: Titulo procurado para fazer a extracao dos dados
    :type titulo_procurado: str
    :return: Retorna uma lista de str contendo todos os dados extraidos.
    :rtype: list[str]
    """

    elements_lista = pegar_elementos_producao(elements, titulo_procurado)
    lista: list[str] = []
    if elements_lista:
        for element in elements_lista:
            try:
                titulo = element.find_all('td')[0].text.strip().replace('\n', '').replace('\t', '').replace('  ','')
                valor = element.find_all('td')[1].text.strip().replace('\n', '').replace('\t', '').replace('  ','')

                if(titulo):
                    lista.append(f'{titulo}: {valor}')
            except:
                pass
        return lista
    return None

def gerar_lista_producao_artigos(elements: Tag, titulo_procurado: str, soup: BeautifulSoup) -> list[str]:
    """
    Gera uma lista contendo todas as informações extraidas dos artigos
    
    :param elements: Tag contendo os elementos para serem iterados
    :type elements: Tag
    :param titulo_procurado: Titulo procurado para fazer a extracao dos dados
    :type titulo_procurado: str
    :param soup: Description
    :type soup: Objeto do Beautiful Soup para fazer a extração dos dados
    :return: Description
    :rtype: list[str]
    """

    elements_lista = pegar_elementos_producao(elements, titulo_procurado)
    lista: list[str] = []
    if elements_lista:
        titulos_elements = elements_lista.select('td')
        id = elements_lista.find('div', class_='chart').get('id')
        lista_valores: list[int] = gerar_lista_valores_grafico(id, soup)
        contador=0
        remover = r'\n\t\xa'
        for element in titulos_elements:
            try:
                titulo = element.text.strip()
                titulo = titulo.translate(str.maketrans('','', remover))
                titulo = ' '.join(titulo.split())
                lista.append(f'{titulo}: {lista_valores[contador]}')
            except Exception as e:
                pass
            finally:
                contador+=1

    return lista

def gerar_lista_valores_grafico(id: str, soup: BeautifulSoup) -> list[int]:
    """
    Extrai os valores dos gráficos e retorna em uma lista de int contendo os valores
    
    :param id: id do grafico a ser extraido
    :type id: str
    :param soup: Objeto do Beautiful Soup para fazer a extracao dos dados
    :type soup: BeautifulSoup
    :return: Retorna uma lista de int contendo todos os valores extraidos do grafico
    :rtype: list[int]
    """

    #Extrai a linha contendo as informações com base no id do grafico
    scripts = "\n".join(sc.get_text() for sc in soup.find_all("script"))
    padrao = re.compile(f"'{id}',[^\n]*")
    resultado = padrao.search(scripts)
    resultado = resultado.group(0).replace(id,'')
    resultado = re.sub(r",\s*,", ",", resultado)
    resultado = resultado.strip("[] ")

    #Extrai apenas números
    numeros = re.findall(r"\d+", resultado)
    lista = [int(n) for n in numeros]
    lista.reverse()
    return lista