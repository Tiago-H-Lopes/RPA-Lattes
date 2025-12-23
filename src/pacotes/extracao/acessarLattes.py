from seleniumbase import SB, BaseCase
from seleniumbase.common.exceptions import NoSuchElementException
from time import sleep
from src.pacotes.utils import escrever_csv, logger
from src.pacotes.utils.nomes_arquivos import PASTA_TEMP, CURRICULO, PRODUCAO, ERRO
import os
import unicodedata
from pathlib import Path

#Função principal
def extrair_dados_lattes(nome: str) -> None:
    """
    Função responsável por extrair o código html das páginas do Lattes para o nome informado, esses códigos serão salvos no diretório atual e utilizados posteriormente para extração de dados.
    
    :param nome: Nome completo a ser pesquisado no site Lattes.
    :type nome: str
    """

    URL = "https://buscatextual.cnpq.br/buscatextual/busca.do"
    MAX_TENTATIVAS = 5
    tentativa_atual = 0

    logger.info(f'Iniciando extração de dados lattes para o nome {nome}')
    while(tentativa_atual < MAX_TENTATIVAS):
        try:
            tentativa_atual += 1
            diretorio_atual = os.curdir
            temp_path = PASTA_TEMP
            temp = os.path.join(diretorio_atual, temp_path)
            lista_diretorio = os.listdir(temp)
            curriculo_nome = CURRICULO.name.replace('{nome}', nome)
            producao_nome = PRODUCAO.name.replace('{nome}', nome)
            producao_path = PRODUCAO.with_name(producao_nome)
            curriculo_path = CURRICULO.with_name(curriculo_nome)
            curriculo = curriculo_path.name
            producao = producao_path.name 

            if curriculo in lista_diretorio and producao in lista_diretorio:
                break

            #Inicia o SeleniumBase
            with SB(uc=True) as sb:
                sb.open(URL)
                sb.maximize_window()

                #Abre a janela do perfil procurado
                sb.type('[name="textoBusca"]', nome)
                sb.click("#botaoBuscaFiltros")
                sleep(3)
                titulo: str = sb.find_element('//div[@class="tit_form"]', by='xpath').text

                #Se não encontrar nenhum resultado para o nome pesquisado
                if titulo.startswith('Nenhum resultado foi encontrado para'):
                    texto = f'Nenhum resultado foi encontrado'
                    escrever_csv(ERRO, nome, texto=texto)
                    logger.warning(f'{texto} para {nome}')
                    break

                #Procura pelo nome informado em todos os nomes que apareceram removendo os acentos dos nomes do site lattes para validar
                nomes_encontrados_elements = sb.find_elements(f'//a', by="xpath")
                lista_nomes_encontrados = []
                for element in nomes_encontrados_elements:
                    nome_original: str = element.text
                    nome_substituido = remover_acentos(nome_original)
                    if(nome_substituido.lower()==nome.lower()):
                        lista_nomes_encontrados.append(nome_original)

                #Se encontrar mais de um resultado, encerra a execução para evitar dados errados
                if len(lista_nomes_encontrados) > 1:
                    texto = f'Muitos resultados encontrados para o nome pesquisado'
                    escrever_csv(ERRO, nome, texto=texto)
                    logger.warning(f'{texto}: {nome}')
                    break

                #Abre a janela pop-up do nome procurado
                nome_procurado = lista_nomes_encontrados[0]
                sb.click(f'//a[text()="{nome_procurado}"]', by="xpath", timeout=30)
                sb.wait_for_element_visible("#idbtnabrircurriculo", timeout=10)

                #Pega os graficos de prd
                grafico_element_existe = sb.is_element_present('iframe.iframe-modal')
                if(not producao in lista_diretorio and grafico_element_existe):
                    logger.debug(f'Extraindo graficos de producao - {nome}')
                    extrair_graficos_producao(sb, nome, producao_path) 
                    sb.switch_to_default_content()    
                
                #abre o curriculo
                if(not curriculo in lista_diretorio):
                    logger.debug(f'Extraindo curriculo - {nome}')
                    extrair_curriculo(sb, nome, curriculo_path)

                loop = False

        except Exception as e:
            logger.error(e)

#Funções auxiliares
def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFD', texto)
    return ''.join([c for c in nfkd if not unicodedata.category(c) == 'Mn'])
 
def extrair_graficos_producao(sb: BaseCase, nome: str, producao_path: Path) -> None:
    """
    Extrai o código html da página contendo os gráficos para o nome informado
    
    :param sb: BaseCase do SeleniumBase para fazer interação com os elementos da página
    :type sb: BaseCase
    :param nome: Nome completo do candidato
    :type nome: str
    :param producao_path: Caminho onde deverá ser salvo o arquivo .html contendo elementos dos gráficos do candidato
    :type producao_path: Path
    """

    try:
        #Muda para o iframe, abre o gráfico e espera carregar para fazer a extração do html da página
        sb.is_element_present('iframe.iframe-modal')
        sb.switch_to_frame('iframe.iframe-modal')
        sb.click("//a[contains(text(), ' Indicadores da Produção')]")
        sb.wait_for_element('canvas.jqplot-base-canvas', timeout=30)
        grafico_abriu = sb.find_element('//h2[@tabindex=0]')
        if grafico_abriu:
            html = sb.get_page_source()
            with open(producao_path, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            raise Exception(f'Falha ao abrir gráfico - {nome}')

    except NoSuchElementException as exception:
        logger.error(f'Elemento não encontrado: {exception}' )
    except Exception as e:
        logger.error(e)

def extrair_curriculo(sb: BaseCase, nome: str, curriculo_path: Path):
    """
    Extrai o código html da página do curriculo do nome informado
    
    :param sb: BaseCase do SeleniumBase para fazer interação com os elementos da página
    :type sb: BaseCase
    :param nome: Nome completo do candidato
    :type nome: str
    :param curriculo_path: Caminho onde deverá ser salvo o código html da página do curriculo do candidato
    :type curriculo_path: Path
    """

    #Abre a página do curriculo, espera carregar, desce até o final da página e faz a extração do html
    sb.click('#idbtnabrircurriculo')
    sleep(2) 
    sb.wait_for_ready_state_complete(timeout=20)
    pagina_abriu = sb.is_element_visible('h2.nome')
    if(pagina_abriu):
        for _ in range(3):
            sleep(2)        
            sb.scroll_to_bottom()
        
        html = sb.get_page_source()       
        with open(curriculo_path, "w", encoding="utf-8") as f:
            f.write(html)
            f.close()

    else:
        logger.warning('Erro ao abrir a página do curriculo')
        raise Exception('Erro ao abrir a página do curriculo')


if __name__ == "__main__":
    nome = 'Carlos assuncao'
    extrair_dados_lattes(nome)