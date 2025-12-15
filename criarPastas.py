import os
import nomes_arquivos as Arquivos

temp = Arquivos.PASTA_TEMP
input = Arquivos.PASTA_INPUT
output = Arquivos.PASTA_OUTPUT

lista_pastas = [temp, input, output]

for pasta in lista_pastas:
    os.makedirs(pasta, exist_ok=True)