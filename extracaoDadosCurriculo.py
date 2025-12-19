from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import escreverCSV
import nomes_arquivos as Arquivos
from pathlib import Path
from logs import logger

def pegarElementosCabecalho(tagName: str, div: Tag) -> list[Tag]:
        if tagName=='ProducoesCientificas':
            producoes_elements_trabalhos: list[Tag] = div.select('div.trab')
            producoes_elements_citacoes: list[Tag] = div.select('div.cita')
            producoes_elements_fator: list[Tag] = div.select('div.fator')
            producoes_elements_detalhes: list[Tag] = div.select('div.detalhes')
            return producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes
        else:
            elements: list[Tag] = div.select('div.layout-cell-pad-5')
            return elements
            

def extrairElemento(elements: list[Tag], informacao_procurada: str) -> str:
    contador = 0
    for element in elements:
        texto: str = element.text
        if texto == informacao_procurada:
            return elements[contador+1].text
        contador += 1



def extrairDadosGerais(div_list: list[Tag], id_lattes: int | str, caminho_pasta_output: Path):
    for div in div_list:
        try:
            dicionario = {}
            tagName = div.find('a').get('name').upper()
            texto = div.select('div.layout-cell-pad-5')
            lista_ignorar_tags = ['identificacao']
            if not texto:
                print(f'{tagName} - Vazio')
                continue
            if tagName.lower() in lista_ignorar_tags:
                continue
            
            print(tagName)
            contador = 0
            dicionario['Titulo'] = tagName
            for t in texto:
                if contador==0:
                    chave = t.text
                    contador += 1
                else:
                    valor: str = t.text
                    valor = valor.replace('\n',' ').replace('\t', '')
                    if valor:
                        dicionario[chave] = valor
                    contador = 0
            if dicionario:

                caminho = caminho_pasta_output / f'LATTES_OUTPUT_{tagName}.csv'
                escreverCSV(caminho, id_lattes, dicionario=dicionario)
        except:
            pass


def extrairDadosArtigos(soup: BeautifulSoup, id_lattes: int | str, caminho: Path):
    resultados = []
    # Todos os <b> que aparecem dentro de um bloco 'cita-artigos'
    for b in soup.select("div.title-wrapper div.cita-artigos > b"):
        cabecalho = b.get_text(strip=True).strip('"')
        if not cabecalho: continue
        valor = None
        

        # Itera pelos elementos à frente deste <b> no fluxo do documento
        for node in b.next_elements:
            if isinstance(node, Tag):
                # Se aparecer um novo bloco 'cita-artigos', encerramos a busca para este cabeçalho
                if node.name == "div" and "cita-artigos" in (node.get("class") or []):
                    break

                if node.name == "div" and "title-wrapper" in (node.get("class") or []):
                    break

                # Se aparecer outro <b> (um novo cabeçalho), também encerramos
                if node.name == "b":
                    continue

                # Primeiro <span class="transform"> encontrado vira o valor
                if node.name == "span" and "transform" in (node.get("class") or []):
                    valor = node.get_text(strip=True)
                    dicionario = {}
                    dicionario[cabecalho] = valor
                    resultados.append(dicionario)
                    continue  # achou o valor, pode parar

    for resultado in resultados:
        escreverCSV(caminho, id_lattes, dicionario=resultado)


def extrairDadosEventos(soup: BeautifulSoup, id_lattes: int | str, caminho: Path):
    resultados = []
    valores = []
    run = False
    # Todos os <b> que aparecem dentro de um bloco 'cita-artigos'
    for b in soup.select("div.title-wrapper div.inst_back > b"):
        cabecalho = b.get_text(strip=True).strip('"')  # remova .strip('"') se quiser manter as aspas
        if cabecalho == 'Participação em eventos, congressos, exposições e feiras':
            run = True
        if run:
            if not cabecalho: continue
            valor = None
            print(cabecalho)

            # Itera pelos elementos à frente deste <b> no fluxo do documento
            for node in b.next_elements:
                if isinstance(node, Tag):
                    # Se aparecer um novo bloco 'inst_back', encerramos a busca para este cabeçalho
                    if node.name == "div" and "inst_back" in (node.get("class") or []):
                        break

                    if node.name == "div" and "title-wrapper" in (node.get("class") or []):
                        break

                    # Se aparecer outro <b> (um novo cabeçalho), também encerramos
                    if node.name == "b":
                        continue

                    # Primeiro <span class="transform"> encontrado vira o valor
                    if node.name == "span" and "transform" in (node.get("class") or []):
                        valor = node.get_text(strip=True)
                        valor = valor.replace('\n', ' ').replace('\t', '')
                        dicionario = {}
                        dicionario[cabecalho] = valor
                        if not valor in valores:
                            valores.append(valor)
                            resultados.append(dicionario)
                        continue  # achou o valor, pode parar

    for resultado in resultados:
        escreverCSV(caminho, id_lattes, dicionario=resultado)


def extrairDadosCurriculo(nome: str):
    logger.debug(f'Extraindo dados do curriculo - {nome}')

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
    escreverCSV(Arquivos.URL_CV, id_lattes, texto=url_cv)
    escreverCSV(Arquivos.ULTIMA_ATUALIZACAO, id_lattes, texto=ultima_atualizacao)
    escreverCSV(Arquivos.RESUMO, id_lattes, texto=resumo)

    div_list = soup.find_all('div', class_='title-wrapper')
    extrairDadosGerais(div_list, id_lattes, Arquivos.PASTA_OUTPUT)
    extrairDadosArtigos(soup, id_lattes, Arquivos.PRODUCOES_ARTIGOS_BANCAS)
    extrairDadosEventos(soup, id_lattes, Arquivos.EVENTOS)


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
            if tagName == 'Identificacao': citacoes_elements = pegarElementosCabecalho(tagName, div)
            if tagName == 'ProducoesCientificas': producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes = pegarElementosCabecalho(tagName, div)
        except:
            pass
            

    #Pega as informações de citações e endereço
    nome_citacoes = extrairElemento(citacoes_elements, 'Nome em citações bibliográficas')
    nacionalidade = extrairElemento(citacoes_elements, 'País de Nacionalidade')
    escreverCSV(Arquivos.NOME_CITACOES, id_lattes, texto=nome_citacoes)
    escreverCSV(Arquivos.NACIONALIDADE, id_lattes, texto=nacionalidade)

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

        escreverCSV(Arquivos.PRODUCOES, id_lattes, lista=lista_producoes)
    

    return id_lattes



if __name__== "__main__":
    extrairDadosCurriculo()