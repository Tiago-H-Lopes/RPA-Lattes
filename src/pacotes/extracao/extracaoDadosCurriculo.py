from pathlib import Path
from bs4.element import Tag
from bs4 import BeautifulSoup
from src.pacotes.utils import escrever_csv, logger
import src.pacotes.utils.nomes_arquivos as Arquivos

#Funcao Principal
def extrair_dados_curriculo(nome: str):
    """
    Extrai os dados do curriculo do nome informado e cria arquivos .csv para cada dado extraido com sucesso
    
    :param nome: Nome completo do candidato
    :type nome: str
    """

    #Le o arquivo e passa o html para o Beautiful Soup
    logger.info(f'Extraindo dados do curriculo - {nome}')
    curriculo_nome = Arquivos.CURRICULO.name.replace('{nome}', nome)
    curriculo = Arquivos.CURRICULO.with_name(curriculo_nome)
    try:
        with open(curriculo, "r", encoding="utf-8") as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(curriculo, "r", encoding="latin-1", errors="strict") as f:
            html = f.read()
    soup = BeautifulSoup(html, 'html.parser')



    #Pega as informações do autor
    ul = soup.find('ul', class_='informacoes-autor')
    li_list = ul.find_all('li')
    url_cv = li_list[0].get_text(strip=True).split(' ')[-1]
    id_lattes = li_list[1].get_text(strip=True).split(':')[-1]
    ultima_atualizacao = li_list[2].get_text(strip=True).split(' ')[-1]
    resumo = soup.find('p', class_='resumo').get_text()
    resumo = resumo.replace('\n', '').strip()
    escrever_csv(Arquivos.URL_CV, id_lattes, texto=url_cv)
    escrever_csv(Arquivos.ULTIMA_ATUALIZACAO, id_lattes, texto=ultima_atualizacao)
    escrever_csv(Arquivos.RESUMO, id_lattes, texto=resumo)

    div_list = soup.find_all('div', class_='title-wrapper')
    extrair_dados_gerais(div_list, id_lattes, Arquivos.PASTA_OUTPUT)
    extrair_dados_artigos(soup, id_lattes, Arquivos.PRODUCOES_ARTIGOS_BANCAS)
    extrair_dados_eventos(soup, id_lattes, Arquivos.EVENTOS)


    #Pega os blocos de elementos da página, como, Identificação, Endereço, Formação Academica, Atução etc
    #Cada item na lista representa um bloco completo com os elementos da página, item 0 = todo o bloco de informações de identificação; item 1 = todo o bloco sobre endereço etc
    citacoes_elements = None
    producoes_elements_trabalhos = None
    producoes_elements_citacoes = None
    producoes_elements_fator = None
    producoes_elements_detalhes = None
    div_list = soup.find_all('div', class_='title-wrapper')
    for div in div_list:
        try:
            tagName = div.find('a').get('name')
            if tagName == 'Identificacao': citacoes_elements = pegar_elementos_cabecalho(tagName, div)
            if tagName == 'ProducoesCientificas': producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes = pegar_elementos_cabecalho(tagName, div)
        except:
            pass
            

    #Pega as informações de citações e endereço
    nome_citacoes = extrair_elemento(citacoes_elements, 'Nome em citações bibliográficas')
    nacionalidade = extrair_elemento(citacoes_elements, 'País de Nacionalidade')
    escrever_csv(Arquivos.NOME_CITACOES, id_lattes, texto=nome_citacoes)
    escrever_csv(Arquivos.NACIONALIDADE, id_lattes, texto=nacionalidade)

    #Gera lista de produções
    if producoes_elements_trabalhos:
        lista_producoes: list[str] = []
        for i in range(len(producoes_elements_trabalhos)):
            try:
                trabalhos = producoes_elements_trabalhos[i].text
                citacoes = producoes_elements_citacoes[i].text
                detalhes = producoes_elements_detalhes[i].text
                fator = producoes_elements_fator[i].text
                lista_producoes.append(f'{trabalhos} | {citacoes} | {fator} | {detalhes}')
            except:
                lista_producoes.append(f'{trabalhos} | {citacoes} | {detalhes}')

        escrever_csv(Arquivos.PRODUCOES, id_lattes, lista=lista_producoes)
    

    return id_lattes

#Funcoes Auxiliares
def pegar_elementos_cabecalho(tagName: str, div: Tag) -> list[Tag]:
    """
    Extrai os elementos de acordo com a tag informada
    
    :param tagName: Tag procurada para extrair os elementos
    :type tagName: str
    :param div: Tag contendo os elementos para serem pesquisados
    :type div: Tag
    :return: Retorna uma lista de Tags contendo todos os elementos encontrados
    :rtype: list[Tag]
    """
    
    if tagName=='ProducoesCientificas':
        producoes_elements_trabalhos: list[Tag] = div.select('div.trab')
        producoes_elements_citacoes: list[Tag] = div.select('div.cita')
        producoes_elements_fator: list[Tag] = div.select('div.fator')
        producoes_elements_detalhes: list[Tag] = div.select('div.detalhes')
        return producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes
    else:
        elements: list[Tag] = div.select('div.layout-cell-pad-5')
        return elements
            
def extrair_elemento(elements: list[Tag], informacao_procurada: str) -> str:
    """
    Procura pelo elemento informado dentro da lista de tags e retorna o .text desse elemento
    
    :param elements: Lista de Tags contendo todos os elementos
    :type elements: list[Tag]
    :param informacao_procurada: Elemento a ser procurado dentro da lista
    :type informacao_procurada: str
    :return: Retorna o .text do elemento procurado
    :rtype: str
    """
    contador = 0
    for element in elements:
        texto: str = element.text
        if texto == informacao_procurada:
            return elements[contador+1].text
        contador += 1

def extrair_dados_gerais(div_list: list[Tag], id_lattes: int | str, caminho_pasta_output: Path):
    """
    Realiza um loop dentro da lista informada, extrai os dados e salva cada um em um arquivo .csv de acordo com 'name' da tag 'a'.
    
    :param div_list: Lista de Tags contendo todos os elementos
    :type div_list: list[Tag]
    :param id_lattes: id_lattes para adicionar no arquivo de output .csv
    :type id_lattes: int | str
    :param caminho_pasta_output: Caminho para a pasta de output para salvar os arquivos gerados
    :type caminho_pasta_output: Path
    """

    for div in div_list:
        try:
            dicionario = {}
            tagName = div.find('a').get('name').upper()
            elementos = div.select('div.layout-cell-pad-5')
            lista_ignorar_tags = ['identificacao']
            if not elementos:
                continue
            if tagName.lower() in lista_ignorar_tags:
                continue
            
            contador = 0
            dicionario['Titulo'] = tagName
            for elemento in elementos:
                if contador==0:
                    chave = elemento.text
                    contador += 1
                else:
                    valor: str = elemento.text
                    valor = valor.replace('\n',' ').replace('\t', '')
                    if valor:
                        dicionario[chave] = valor
                    contador = 0
            if dicionario:

                caminho = caminho_pasta_output / f'LATTES_OUTPUT_{tagName}.csv'
                escrever_csv(caminho, id_lattes, dicionario=dicionario)
        except:
            pass

def extrair_dados_artigos(soup: BeautifulSoup, id_lattes: int | str, caminho: Path):
    """
    Extrai todos os dados da parte de 'Artigos' do curriculo
    
    :param soup: Obejto do bs4 com o código completo da página para fazer a extração dos dados
    :type soup: BeautifulSoup
    :param id_lattes: id_lattes para escrever no arquivo .csv de output
    :type id_lattes: int | str
    :param caminho: Caminho para salvar o arquivo contendo as informações extraida dos artigos
    :type caminho: Path
    """

    # Procura todas as Tags <b> que venham logo após um div.cita-artigos
    resultados = []
    for b in soup.select("div.title-wrapper div.cita-artigos > b"):
        cabecalho = b.get_text(strip=True).strip('"')
        if not cabecalho: continue
        valor = None
        

        # Itera pelos elementos à frente deste <b> no fluxo do documento
        for node in b.next_elements:
            if isinstance(node, Tag):

                # Se aparecer um novo bloco 'cita-artigos' ou 'title-wrapper', encerra a busca para este cabeçalho
                if node.name == "div" and "cita-artigos" in (node.get("class") or []):
                    break
                if node.name == "div" and "title-wrapper" in (node.get("class") or []):
                    break

                # Se aparecer outro <b> (um novo cabeçalho), também será encerrado
                if node.name == "b":
                    continue

                # Tag <span> com a class transform contém os valores a serem extraidos
                if node.name == "span" and "transform" in (node.get("class") or []):
                    valor = node.get_text(strip=True)
                    dicionario = {}
                    dicionario[cabecalho] = valor
                    resultados.append(dicionario)
                    continue

    for resultado in resultados:
        escrever_csv(caminho, id_lattes, dicionario=resultado)

def extrair_dados_eventos(soup: BeautifulSoup, id_lattes: int | str, caminho: Path):
    """
    Extrai todos os dados da parte de 'Eventos' do curriculo
    
    :param soup: Obejto do bs4 com o código completo da página para fazer a extração dos dados
    :type soup: BeautifulSoup
    :param id_lattes: id_lattes para escrever no arquivo .csv de output
    :type id_lattes: int | str
    :param caminho: Caminho para salvar o arquivo contendo as informações extraida dos artigos
    :type caminho: Path
    """
    resultados = []
    valores = []
    run = False
    # Filtra por todas as tags <b> que aparecerm logo após um div com a class inst_back
    for b in soup.select("div.title-wrapper div.inst_back > b"):
        cabecalho = b.get_text(strip=True).strip('"')
        # Começa a pesquisar os dados somente após encontrar esse cabecalho
        if cabecalho == 'Participação em eventos, congressos, exposições e feiras':
            run = True

        if run:
            if not cabecalho: continue
            valor = None
            # Itera pelos elementos à frente deste <b> no fluxo do documento
            for node in b.next_elements:
                if isinstance(node, Tag):

                    # Se aparecer um novo bloco 'inst_back' ou 'title-wrappe', encerra a busca para esse cabecalho
                    if node.name == "div" and "inst_back" in (node.get("class") or []):
                        break
                    if node.name == "div" and "title-wrapper" in (node.get("class") or []):
                        break

                    # Se aparecer outro <b> (um novo cabeçalho), também será encerrado 
                    if node.name == "b":
                        continue

                    # A Tag <span class="transform"> é a que contém os valroes a serem extraidos
                    if node.name == "span" and "transform" in (node.get("class") or []):
                        valor = node.get_text(strip=True)
                        valor = valor.replace('\n', ' ').replace('\t', '')
                        dicionario = {}
                        dicionario[cabecalho] = valor
                        if not valor in valores:
                            valores.append(valor)
                            resultados.append(dicionario)
                        continue

    for resultado in resultados:
        escrever_csv(caminho, id_lattes, dicionario=resultado)



if __name__== "__main__":
    extrair_dados_curriculo()