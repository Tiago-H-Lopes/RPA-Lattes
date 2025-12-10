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
            print(tentativa_atual)
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
                sb.type('input[name="textoBusca"]', nome)
                sb.click("#botaoBuscaFiltros")
                sleep(3)
                primeiro_nome = nome.split(' ')[0].capitalize()
                titulo: str = sb.find_element('//div[@class="tit_form"]', by='xpath').text

                #Se não encontrar nenhum resultado para o nome pesquisado
                if titulo.startswith('Nenhum resultado foi encontrado para'):
                    texto = f'Nenhum resultado foi encontrado'
                    escreverCSV(Arquivos.ERRO.value, nome, texto=texto)
                    break

                sb.click(f'//a[starts-with(text(), "{primeiro_nome}")]', by="xpath", timeout=30)
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
            print(e)

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
            raise Exception('Falha ao abrir gráfico')

    except NoSuchElementException as exception:
        print(f'Elemento não encontrado: {exception}' )
    except Exception as e:
        print(e)


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
        raise Exception('Erro ao abrir a página do curriculo')


if __name__ == "__main__":
    nome = 'ALINE FERNANDES DE SA FINTELMAM'
    extrairDadosLattes(nome)