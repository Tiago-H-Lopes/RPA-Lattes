from pathlib import Path

def escrever_csv(arquivo: Path, id_lattes: str, lista: list[str] = None, texto: str = None, dicionario: dict = None):    
    """
    Escreve um arquivo csv para o caminho informado, usando como base de dados o que for passado, podendo ser uma lista, uma string ou um dict
    
    :param arquivo: Caminho do arquivo a ser escrito
    :type arquivo: Path
    :param id_lattes: id_lattes do candidato
    :type id_lattes: str
    :param lista: Lista contendo os valores a serem escritos
    :type lista: list[str] | None
    :param texto: String contendo o valor a ser escrito
    :type texto: str | None
    :param dicionario: Dict no formato 'cabeçalho: valor' para ser escrito
    :type dicionario: dict | None
    """

    if(lista==None and texto==None and dicionario==None):
        return
    with open(arquivo, 'a+', encoding='utf-8') as csv:
        titulo = ''

        # Le a primeira linha do arquivo, se não encontrar nada, gera um cabeçalho 
        csv.seek(0)
        texto_csv = csv.readline()
        if texto_csv=='':
            if not dicionario:
                nome_arquivo = arquivo.name
                titulo = nome_arquivo.replace('LATTES_OUTPUT_', '').replace('.csv', '')
                csv.write(f'LATTES_ID; {titulo}\n')
            else:
                csv.write(f'LATTES_ID; TITULO; CHAVE; VALOR\n')
        
        # Vai para a última linha do arquivo para adicionar os novos dados
        csv.seek(0, 2)
        if lista:
            for item in lista:
                csv.write(f'{id_lattes}; "{item}"\n')

        if texto:
                csv.write(f'{id_lattes}; "{texto}"\n')

        if dicionario:
            for chave, valor in dicionario.items():
                # Atribui o valor da chave atual para chave anterior para os casos onde a chave 
                # fica pendente porém os dados fazem parte do mesmo bloco
                if chave:
                    chave_anterior = chave
                if not titulo:
                    titulo = chave_anterior
                    
                if chave=='Titulo':
                    titulo = valor
                else:
                    csv.write(f'{id_lattes}; {titulo}; "{chave_anterior}"; "{valor}"\n')