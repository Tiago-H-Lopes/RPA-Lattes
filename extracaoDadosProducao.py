from bs4 import BeautifulSoup, Tag
from utils import gerarListaProducao, gerarListaProducaoArtigos, escreverCSV
from nomes_arquivos_enum import Arquivos

def extrairDadosProducao(id_lattes: str) -> None:
    producao = Arquivos.PRODUCAO.value
    with open(producao, encoding='utf-8') as document:
        html = document.read()

    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('div', class_='grafico')

    if elements:
        lista_prod_bibliograficas = gerarListaProducao(elements, 'Produção Bibliográfica')
        lista_prod_tecnica = gerarListaProducao(elements, 'Produção Técnica')
        lista_orientacoes = gerarListaProducao(elements, 'Orientações Concluídas')
        lista_todas_prod = gerarListaProducao(elements, 'Todas as Produções')
        lista_artigos = gerarListaProducaoArtigos(elements, 'Total de Artigos Publicados por Periódico', soup)

    if lista_prod_bibliograficas:
        escreverCSV(Arquivos.PRODUCOES_BIBLIOGRAFICAS.value, id_lattes, lista_prod_bibliograficas)

    if lista_prod_tecnica:
        escreverCSV(Arquivos.PRODUCOES_TECNICAS.value, id_lattes, lista_prod_tecnica)

    if lista_orientacoes:
        escreverCSV(Arquivos.ORIENTACOES.value, id_lattes, lista_orientacoes)

    if lista_todas_prod:
        escreverCSV(Arquivos.TODAS_PRODUCOES.value, id_lattes, lista_todas_prod)
        
    if lista_artigos:
        escreverCSV(Arquivos.ARTIGOS_PRODUCAO.value, id_lattes, lista_artigos)