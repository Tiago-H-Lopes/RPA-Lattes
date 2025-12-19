from bs4 import BeautifulSoup, Tag
from utils import gerarListaProducao, gerarListaProducaoArtigos, escreverCSV
import nomes_arquivos as Arquivos
from logs import logger

def extrairDadosProducao(id_lattes: int | str, nome: str) -> None:
    logger.debug(f'Extraindo dado producao - {nome}')

    producao_nome = Arquivos.PRODUCAO.name.replace('{nome}', nome)
    producao = Arquivos.PRODUCAO.with_name(producao_nome)
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
        escreverCSV(Arquivos.PRODUCOES_BIBLIOGRAFICAS, id_lattes, lista_prod_bibliograficas)

    if lista_prod_tecnica:
        escreverCSV(Arquivos.PRODUCOES_TECNICAS, id_lattes, lista_prod_tecnica)

    if lista_orientacoes:
        escreverCSV(Arquivos.ORIENTACOES, id_lattes, lista_orientacoes)

    if lista_todas_prod:
        escreverCSV(Arquivos.TODAS_PRODUCOES, id_lattes, lista_todas_prod)
        
    if lista_artigos:
        escreverCSV(Arquivos.ARTIGOS_PRODUCAO, id_lattes, lista_artigos)