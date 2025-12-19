import os
import criarPastas
import logs
from utils import escreverCSV
from acessarLattes import extrairDadosLattes
from deletarArquivos import deletarArquivosTemporarios
from extracaoDadosProducao import extrairDadosProducao
from extracaoDadosCurriculo import extrairDadosCurriculo
from extracaoDadosDiretorio import extrairDadosDiretorio
from processados import NomeProcessado, AnotarNomeProcessado
from nomes_arquivos import PASTA_TEMP, CURRICULO, PRODUCAO, ERRO, INPUT, NOMES_IDS
from logs import logger
import csv
from multiprocessing import Pool, cpu_count


def main(nome: str):
    #Variaveis contendo o caminho da pasta temp e os nomes dos arquivos com as extensões
    temp = PASTA_TEMP
    curriculo = CURRICULO.name
    producao = PRODUCAO.name
    curriculo = curriculo.replace('{nome}', nome)
    producao = producao.replace('{nome}', nome)
    csv_erro = ERRO

    extrairDadosLattes(nome)
    lista_arquivos = os.listdir(temp)
    if curriculo in lista_arquivos:
        id_lattes = extrairDadosCurriculo(nome)
        extrairDadosDiretorio(id_lattes)
        escreverCSV(NOMES_IDS, id_lattes, texto=nome)

        
        if producao in lista_arquivos:
            extrairDadosProducao(id_lattes, nome)  
            logger.info('Processado com sucesso')      
            AnotarNomeProcessado(nome)    
    else:
        escreverCSV(csv_erro, nome, texto='Não foi possivel baixar o curriculo')
        logger.warning(f'Não foi possivel acessar o curriculo de {nome}')
        AnotarNomeProcessado(nome)

def worker(nome: str) -> tuple[str, bool, str | None]:
    try:
        main(nome)
        return (nome, True, None)
    except Exception as e:
        return (nome, False, str(e))

def carregar_nomes(input_csv: str, max_linhas: int | None = None) -> list[str]:
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

# if __name__== "__main__":
#     logger.info('Execução iniciada')
#     input_csv = INPUT
    
#     with open(input_csv) as csv:
#         row = csv.readline()
#         # while(row):

#         for _ in range(10):
#             # try:
#                 nome = csv.readline().strip()
#                 if not NomeProcessado(nome):
#                     logger.info(f'Processando {nome}')
#                     deletarArquivosTemporarios(nome)
#                     main(nome)
                    
            # except Exception as e:
            #     logger.error(e)
            #     continue

            

if __name__ == "__main__":
    logger.info("Execução iniciada")
    deletarArquivosTemporarios()
    nomes = carregar_nomes(INPUT, max_linhas=10)
    nomes_a_processar = [n for n in nomes if not NomeProcessado(n)]
    logger.info(f"Total a processar: {len(nomes_a_processar)}")

    if not nomes_a_processar:
        logger.info("Nada a processar.")
        raise SystemExit(0)

    processos = min(cpu_count() or 2, len(nomes_a_processar))
    chunksize = max(1, len(nomes_a_processar) // (processos * 2))  # ajuste prático

    with Pool(processes=processos) as pool:
        for nome, sucesso, erro in pool.imap_unordered(worker, nomes_a_processar, chunksize=chunksize):
            if sucesso:
                logger.info(f"✔ Processado: {nome}")
            else:
                logger.error(f"✖ Falha em {nome}: {erro}")

    deletarArquivosTemporarios()
    logger.info("Concluído.")
