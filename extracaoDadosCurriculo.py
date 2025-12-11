from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import gerarListaAtuacao, gerarListaPadrao, pegarElementosCabecalho, escreverCSV
from nomes_arquivos_enum import Arquivos


def extrairElemento(elements: list[Tag], informacao_procurada: str) -> str:
    contador = 0
    for element in elements:
        texto: str = element.text
        if texto == informacao_procurada:
            return element[contador+1].text
        contador += 1

def extrairDadosCurriculo():
    curriculo = Arquivos.CURRICULO.value
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

    #Pega os blocos de elementos da página, como, Identificação, Endereço, Formação Academica, Atução etc
    #Cada item na lista representa um bloco completo com os elementos da página, item 0 = todo o bloco de informações de identificação; item 1 = todo o bloco sobre endereço etc
    div_list = soup.find_all('div', class_='title-wrapper')
    citacoes_elements, endereco_elements, formacao_academica_elements, formacao_complementar_elements, atuacao_profissional_elements, area_atuacao_elements, idiomas_elements, premios_elements, producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes, artigos_elements = (None,)*13
    for div in div_list:
        try:
            tagName = div.find('a').get('name')
            match tagName:
                case 'Identificacao': citacoes_elements = pegarElementosCabecalho(tagName, div)
                case 'Endereco': endereco_elements = pegarElementosCabecalho(tagName, div)
                case 'FormacaoAcademicaTitulacao': formacao_academica_elements = pegarElementosCabecalho(tagName, div)
                case 'FormacaoComplementar': formacao_complementar_elements = pegarElementosCabecalho(tagName, div)
                case 'AtuacaoProfissional': atuacao_profissional_elements = pegarElementosCabecalho(tagName, div)
                case 'AreasAtuacao': area_atuacao_elements = pegarElementosCabecalho(tagName, div)
                case 'Idiomas': idiomas_elements = pegarElementosCabecalho(tagName, div)
                case 'PremiosTitulos': premios_elements = pegarElementosCabecalho(tagName, div)
                case 'ProducoesCientificas': producoes_elements_trabalhos, producoes_elements_citacoes, producoes_elements_fator, producoes_elements_detalhes, artigos_elements = pegarElementosCabecalho(tagName, div)
        except:
            pass
            

    #Pega as informações de citações e endereço
    nome_citacoes = extrairElemento(citacoes_elements, 'Nome em citações bibliográficas')
    nacionalidade = extrairElemento(citacoes_elements, 'País de Nacionalidade')
    endereco_profissional = extrairElemento(endereco_elements, 'Endereço Profissional')

    #Gera lista com as principais formações academicas
    if formacao_academica_elements:
        lista_formacoes: list[str] = gerarListaPadrao(formacao_academica_elements)

    #Gera lista com as formações complementares
    if formacao_complementar_elements:
        lista_formacoes_complementares: list[str] = gerarListaPadrao(formacao_complementar_elements)

    #Gera lista com as atuações profissionais
    if atuacao_profissional_elements:
        atuacao_profissional_elements = atuacao_profissional_elements[2:]
        lista_atuacoes_profissionais: list[str] = gerarListaAtuacao(atuacao_profissional_elements)

    #Gera lista com as áreas de atuação
    #A conversao para int serve apenas para ignorar a numeração das áreas de atuação e extrair somente o texto relevante
    lista_area_atuacao: list[str] = []
    if area_atuacao_elements:
        for element in area_atuacao_elements:
            texto = element.text
            try:
                texto = int(texto[0])
            except:
                lista_area_atuacao.append(texto)

    #Gera lista com os idiomas falados
    if idiomas_elements:
        lista_idiomas: list[str] = gerarListaPadrao(idiomas_elements)

    #Gera lista com os premios recebidos
    if premios_elements:
        lista_premios: list[str] = gerarListaPadrao(premios_elements)

    #Gera lista de produções
    lista_producoes: list[str] = []
    if producoes_elements_trabalhos:
        for i in range(len(producoes_elements_trabalhos)):
            try:
                trabalhos = producoes_elements_trabalhos[i].text
                citacoes = producoes_elements_citacoes[i].text
                detalhes = producoes_elements_detalhes[i].text
                fator = producoes_elements_fator[i].text
                lista_producoes.append(f'{trabalhos} | {citacoes} | {fator} | {detalhes}')
            except:
                lista_producoes.append(f'{trabalhos} | {citacoes} | {detalhes}')

    #Gera lista de Artigos
    lista_artigos: list[str] = []
    if artigos_elements:
        for element in artigos_elements:
            texto: str = element.text.replace('\n', '').replace('\t', '')
            lista_artigos.append(texto)
    
    escreverCSV(Arquivos.URL_CV.value, id_lattes, texto=url_cv)
    escreverCSV(Arquivos.ULTIMA_ATUALIZACAO.value, id_lattes, texto=ultima_atualizacao)
    escreverCSV(Arquivos.RESUMO.value, id_lattes, texto=resumo)
    escreverCSV(Arquivos.NOME_CITACOES.value, id_lattes, texto=nome_citacoes)
    escreverCSV(Arquivos.NACIONALIDADE.value, id_lattes, texto=nacionalidade)
    escreverCSV(Arquivos.ENDERECO_PROFISSIONAL.value, id_lattes, texto=endereco_profissional)

    escreverCSV(Arquivos.FORMACOES.value, id_lattes, lista=lista_formacoes)
    escreverCSV(Arquivos.FORMACOES_COMPLEMENTARES.value, id_lattes, lista=lista_formacoes_complementares)
    escreverCSV(Arquivos.ATUACOES_PROFISSIONAIS.value, id_lattes, lista=lista_atuacoes_profissionais)
    escreverCSV(Arquivos.AREA_ATUACAO.value, id_lattes, lista=lista_area_atuacao)
    escreverCSV(Arquivos.IDIOMAS.value, id_lattes, lista=lista_idiomas)
    escreverCSV(Arquivos.PREMIOS.value, id_lattes, lista=lista_premios)
    escreverCSV(Arquivos.PRODUCOES.value, id_lattes, lista=lista_producoes)
    escreverCSV(Arquivos.ARTIGOS_CURRICULO.value, id_lattes, lista=lista_artigos)

if __name__== "__main__":
    extrairDadosCurriculo()