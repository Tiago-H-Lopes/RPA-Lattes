from seleniumbase import SB, BaseCase
from seleniumbase.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from utils import escreverCSV
from nomes_arquivos_enum import Arquivos
import os
import unicodedata
from logs import logger

def remover_acentos(texto):
    # Normaliza o texto para a forma NFD (decomposição)
    nfkd = unicodedata.normalize('NFD', texto)
    # Filtra apenas os caracteres que não são marcas de acento (Mn = Mark, Nonspacing)
    return ''.join([c for c in nfkd if not unicodedata.category(c) == 'Mn'])

def extrairDadosLattes(nome: str) -> None:
    """
    Função responsável por extrair o código html das páginas do Lattes para o nome informado, esses códigos serão salvos no diretório atual e utilizados posteriormente para extração de dados.
    
    :param nome: Nome completo a ser pesquisado no site Lattes.
    :type nome: str
    """

    URL = "https://buscatextual.cnpq.br/buscatextual/busca.do"
    MAX_TENTATIVAS = 5
    tentativa_atual = 0

    while(tentativa_atual < MAX_TENTATIVAS):
        try:
            tentativa_atual += 1
            diretorio_atual = os.curdir
            temp_path = Arquivos.PASTA_TEMP.value
            temp = os.path.join(diretorio_atual, temp_path)
            lista_diretorio = os.listdir(temp)
            curriculo = Arquivos.CURRICULO.value
            producao = Arquivos.PRODUCAO.value
            curriculo = curriculo.split('/')[-1]
            producao = producao.split('/')[-1]

            if curriculo in lista_diretorio and producao in lista_diretorio:
                break

            with SB(uc=True) as sb:
                sb.open(URL)
                sb.maximize_window()

                #Abre a janela do perfil procurado
                sb.type('[name="textoBusca"]', nome)
                sb.click("#botaoBuscaFiltros")
                sleep(3)
                primeiro_nome = nome.split(' ')[0].capitalize()
                titulo: str = sb.find_element('//div[@class="tit_form"]', by='xpath').text

                #Se não encontrar nenhum resultado para o nome pesquisado
                if titulo.startswith('Nenhum resultado foi encontrado para'):
                    texto = f'Nenhum resultado foi encontrado'
                    escreverCSV(Arquivos.ERRO.value, nome, texto=texto)
                    logger.warning(f'{texto} para {nome}')
                    break

                nomes_encontrados_elements = sb.find_elements(f'//a', by="xpath")
                lista_nomes_encontrados = []
                for element in nomes_encontrados_elements:
                    nome_original: str = element.text
                    nome_substituido = remover_acentos(nome_original)
                    if(nome_substituido.lower()==nome.lower()):
                        lista_nomes_encontrados.append(nome_original)

                if len(lista_nomes_encontrados) > 1:
                    texto = f'Muitos resultados encontrados para o nome pesquisado'
                    escreverCSV(Arquivos.ERRO.value, nome, texto=texto)
                    logger.warning(f'{texto}: {nome}')
                    break

                nome_procurado = lista_nomes_encontrados[0]
                sb.click(f'//a[text()="{nome_procurado}"]', by="xpath", timeout=30)
                sb.wait_for_element_visible("#idbtnabrircurriculo", timeout=10)

                #Pega os graficos de prd
                grafico_element_existe = sb.is_element_present('iframe.iframe-modal')
                if(not 'producao.html' in lista_diretorio and grafico_element_existe):
                    extrairGraficosProducao(sb) 
                    sb.switch_to_default_content()    
                
                #abre o curriculo
                if(not 'curriculo.html' in lista_diretorio):
                    extrairCurriculo(sb)

                loop = False

        except Exception as e:
            logger.error(e)

def extrairGraficosProducao(sb: BaseCase):
    try:
        sb.is_element_present('iframe.iframe-modal')
        sb.switch_to_frame('iframe.iframe-modal')
        sb.click("//a[contains(text(), ' Indicadores da Produção')]")
        sb.wait_for_element('canvas.jqplot-base-canvas', timeout=30)
        grafico_abriu = sb.find_element('//h2[@tabindex=0]')
        if grafico_abriu:
            html = sb.get_page_source()
            with open(Arquivos.PRODUCAO.value, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            logger.warning('Falha ao abrir o gráfico')
            raise Exception('Falha ao abrir gráfico')

    except NoSuchElementException as exception:
        logger.error(f'Elemento não encontrado: {exception}' )
    except Exception as e:
        logger.error(e)


def extrairCurriculo(sb: BaseCase):
    sb.click('#idbtnabrircurriculo')
    sleep(2) 

    sb.wait_for_ready_state_complete(timeout=20)  # Para garantir que está no CV e que a página está completamente carregada
    pagina_abriu = sb.is_element_visible('h2.nome')
    if(pagina_abriu):
        for _ in range(3):
            sleep(2)        
            sb.scroll_to_bottom()
        
        html = sb.get_page_source()       
        with open(Arquivos.CURRICULO.value, "w", encoding="utf-8") as f:
            f.write(html)
            f.close()
    else:
        logger.warning('Erro ao abrir a página do curriculo')
        raise Exception('Erro ao abrir a página do curriculo')


if __name__ == "__main__":
    nome = 'Carlos assuncao'
    extrairDadosLattes(nome)