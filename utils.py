from bs4 import Tag, BeautifulSoup
import re
from pathlib import Path

def pegarElementosCabecalho(tagName: str, div: Tag) -> list[Tag]:
    #Lista com tags que seguem o mesmo padrão de extração
    lista_tags_padrao = ['Identificacao', 'Endereco', 'FormacaoAcademicaTitulacao', 'FormacaoComplementar', 'AtuacaoProfissional', 'AreasAtuacao', 'Idiomas', 'PremiosTitulos']
    match tagName:
        case x if x in (lista_tags_padrao):
            elements: list[Tag] = div.select('div.layout-cell-pad-5')
            return elements
        case x if x=='ProducoesCientificas':
            producoes_elements_trabalhos: list[Tag] = div.select('div.trab')
            producoes_elements_citacoes: list[Tag] = div.select('div.cita')
            producoes_elements_fator: list[Tag] = div.select('div.fator')
            producoes_elements_detalhes: list[Tag] = div.select('div.detalhes')
            artigos_elements: list[Tag] = div.select('span.transform')
            return producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes, artigos_elements
        case _:
            pass

def gerarListaPadrao(elements: list[Tag]) -> list [str]:    
    """
    Gera uma lista padrão com 2 elementos separados sendo geralmente [{ano | descrição}] de acordo com os elementos html enviados.

    Args:
        elements (list[Tag]): Lista de elementos html a serem percorridos.

    Returns:
        list[str]: Lista com [{ano | descrição}] de todos os elementos.
    """
    contador=0
    lista: list[str] = []
    for element in elements:
        if(contador==0):
            ano_formacao = element.text
            contador += 1
        else:
            formacao: str = element.text
            formacao = formacao.replace('\n', ' ').replace('\t', '')  
            if(len(formacao)>0):      
                lista.append(f'{ano_formacao}  |  {formacao}')
            contador -= 1
    return lista


def gerarListaAtuacao(elements: list[Tag]) -> list [str]:    
    """
    Gera uma lista com [{ano | atuação | Outras Informações}] de acordo com os elementos html enviados.

    Args:
        elements (list[Tag]): Lista de elementos html a serem percorridos.

    Returns:
        list[str]: Lista com [{ano | atuação | Outras Informações}] de todos os elementos.
    """
    lista: list[str] = []
    texto: str = ''
    for element in elements:
        texto_elemento = element.text
        if(texto_elemento==''): continue
        if(texto_elemento.startswith('Outras informa')): continue

        if(texto_elemento.endswith('institucional')): 
            texto = texto.replace('\n', ' ').replace('\t', '')
            lista.append(texto[:-3])
            texto = ''
            continue

        texto += element.text
        texto += ' | '
    return lista

def gerarListaAreaAtuacao(elements: list[Tag]) -> list[str]:
    lista: list[str] = []
    for element in elements:
        texto = element.text
        if(not isinstance(texto[0], int)):
            lista.append(element.text)

def gerarListaDiretorio(elements: list[Tag], contador_limite: int):
    texto: str = ''
    lista: list[str] = []
    contador: int = 0
    for row in elements:
        if(contador<contador_limite):
            texto += row.text + ' | '
            contador += 1
        else:
            lista.append(texto[:-3])
            contador = 0
            texto = ''
    return lista

def pegarElementosProducao(elements: Tag, titulo_procurado: str) -> Tag:
    for element in elements:
        titulo: str = element.select_one('h2').text
        titulo = titulo.strip()

        if(titulo==titulo_procurado and titulo_procurado=='Total de Artigos Publicados por Periódico'):
            return element.select_one('div.layout-cell.layout-cell-12')
        
        if(titulo==titulo_procurado):
            return element.select_one('tbody')

def gerarListaProducao(elements: Tag, titulo_procurado: str) -> list[str]:
    elements_lista = pegarElementosProducao(elements, titulo_procurado)
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

def geraListaValoresGrafico(id: str, soup: BeautifulSoup) -> list[int]:
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

def gerarListaProducaoArtigos(elements: Tag, titulo_procurado: str, soup: BeautifulSoup) -> list[str]:
    elements_lista = pegarElementosProducao(elements, titulo_procurado)
    lista: list[str] = []
    if elements_lista:
        titulos_elements = elements_lista.select('td')
        id = elements_lista.find('div', class_='chart').get('id')
        lista_valores: list[int] = geraListaValoresGrafico(id, soup)
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

def escreverCSV(arquivo: Path, id_lattes: str, lista: list[str] = None, texto: str = None):    
    if(lista==None and texto==None):
        return
    with open(arquivo, 'a+', encoding='utf-8') as csv:

        csv.seek(0)
        texto_csv = csv.readline()
        if texto_csv=='':
            nome_arquivo = arquivo.name
            titulo = nome_arquivo.replace('LATTES_OUTPUT_', '').replace('.csv', '')
            csv.write(f'LATTES_ID; {titulo}\n')
        
        csv.seek(0, 2)
        if lista:
            for item in lista:
                csv.write(f'{id_lattes}; "{item}"\n')
        if texto:
                csv.write(f'{id_lattes}; "{texto}"\n')