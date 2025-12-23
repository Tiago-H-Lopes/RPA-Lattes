import os
import csv
import subprocess
from pathlib import Path
from multiprocessing import Pool, cpu_count
from src.pacotes.utils.nomes_arquivos import PASTA_TEMP, CURRICULO, PRODUCAO, ERRO, INPUT, NOMES_IDS
from src.pacotes.extracao import extrair_dados_diretorio, extrair_dados_curriculo, extrair_dados_producao, extrair_dados_lattes
from src.pacotes.utils import criar_pastas, escrever_csv, nome_processado, anotar_nome_processado, deletar_arquivos_temporarios, logger

#Fluxo principal
def main(nome: str):
    #Variaveis contendo o caminho da pasta temp e os nomes dos arquivos com as extensões
    temp = PASTA_TEMP
    curriculo = CURRICULO.name
    producao = PRODUCAO.name
    curriculo = curriculo.replace('{nome}', nome)
    producao = producao.replace('{nome}', nome)
    csv_erro = ERRO

    #Inicio do processamento abrindo o site do lattes para baixar o curriculo e extrair os graficos
    extrair_dados_lattes(nome)
    lista_arquivos = os.listdir(temp)
    if curriculo in lista_arquivos:
        id_lattes = extrair_dados_curriculo(nome)
        extrair_dados_diretorio(id_lattes)
        escrever_csv(NOMES_IDS, id_lattes, texto=nome)
       
        if producao in lista_arquivos:
            extrair_dados_producao(id_lattes, nome)  
            anotar_nome_processado(nome)    
            logger.info(f'Processado com sucesso - {nome}')      
    else:
        escrever_csv(csv_erro, nome, texto='Não foi possivel baixar o curriculo')
        anotar_nome_processado(nome)

#Worker para multiprocessamento
def worker(nome: str) -> tuple[str, bool, str | None]:
    try:
        main(nome)
        return (nome, True, None)
    except Exception as e:
        return (nome, False, str(e))

#Leitura da planilha de input
def carregar_nomes(input_csv: Path, max_linhas: int | None = None) -> list[str]:
    """
    Lê os nomes na planilha de input. Se max_linhas for definido, lerá a quantidade informada, começando pelo primeiro nome, se nenhuma quantidade for informada, lerá o arquivo inteiro.
    
    :param input_csv: Caminho para o arquivo de input
    :type input_csv: Path
    :param max_linhas: Limite de nomes para serem lidos do arquivo de input, deixar em branco se quiser ler a planilha completa
    :type max_linhas: int | None
    :return: Lista contendo todos os nomes extraidos do arquivo da input
    :rtype: list[str]
    """
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # cabeçalho
        except StopIteration:
            return []
        nomes = []
        for i, row in enumerate(reader):
            if max_linhas is not None and i >= max_linhas:
                break
            if row:
                nomes.append(row[0].strip())
        return [n for n in nomes if n]          

if __name__ == "__main__":
    #Cria pastas, encerra o chrome, deleta arquivos temporarios e filtra os nomes apenas pelos não processados
    criar_pastas()
    logger.info("Execução iniciada")
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/T"], check=False)
    deletar_arquivos_temporarios()
    nomes = carregar_nomes(INPUT, max_linhas=50)
    nomes_a_processar = [n for n in nomes if not nome_processado(n)]
    logger.info(nomes_a_processar)
    logger.info(f"Total a processar: {len(nomes_a_processar)}")

    if not nomes_a_processar:
        logger.info("Nada a processar.")
        raise SystemExit(0)

    #Parametros para o multiprocessamento
    processos = min(cpu_count() or 2, len(nomes_a_processar))
    chunksize = max(1, len(nomes_a_processar) // (processos * 2))
    resultados = []

    with Pool(processes=processos) as pool:
        logger.info(f'Iniciando a pool para {processos} processos, com {chunksize} de chunksize')
        for nome, _, _ in pool.imap_unordered(worker, nomes_a_processar, chunksize=chunksize):
            logger.info(f'Fim do processamento de {nome}')
            resultados.append(nome)

    #Deleta os arquivos temporarios e encerra o chrome
    logger.info(f'Nomes processados: {resultados}')
    deletar_arquivos_temporarios()
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/T"], check=False)
    logger.info("Execução finalizada com sucesso.")
