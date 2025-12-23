
# 📘 RPA Extração de Dados Lattes

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Automation](https://img.shields.io/badge/RPA-Automation-orange)
![Multiprocessing](https://img.shields.io/badge/Multiprocessing-Enabled-purple)

Ferramenta de automação (RPA) desenvolvida para **extrair dados da plataforma Lattes** de forma massiva, rápida e resiliente, superando as limitações impostas pelo site e otimizando o processamento por meio de **multiprocessamento em Python**.

O sistema recebe um arquivo `.csv` com uma lista de nomes, acessa cada currículo Lattes correspondente e exporta os dados estruturados em **arquivos CSV individuais**, um para cada tipo de dado coletado (identificação, endereço, formação, histórico profissional, produção acadêmica, eventos, etc.).  
Além disso, o processo mantém logs detalhados e registra quais nomes já foram processados.

---

## 🧠 Objetivo do Projeto

- Automatizar a extração de informações públicas da plataforma Lattes.  
- Processar **grandes listas de nomes** utilizando multiprocessamento para ganho de desempenho.  
- Superar limitações de acesso, tempo de resposta e restrições da plataforma Lattes.  
- Gerar dados estruturados em arquivos `.csv` individuais para fácil análise posterior.

---

## ⚙️ Principais Funcionalidades

- 📥 Leitura de arquivo de entrada `.csv` contendo nomes a serem pesquisados.  
- 🔍 Acesso automatizado aos currículos Lattes.  
- 📊 Extração de:
  - Identificação  
  - Endereço  
  - Formação acadêmica  
  - Histórico profissional  
  - Produção bibliográfica (artigos, livros, capítulos etc.)  
  - Atividades de mentoria  
  - Participação em eventos  
  - Outros dados relevantes do currículo  
- ⚡ Multiprocessamento para acelerar a coleta.  
- 🚫 Tratativas contra limitações e bloqueios do site.  
- 🗂 Geração de arquivos CSV organizados por tipo de dado.  
- 📝 Logs detalhados e controle de nomes já processados.

---

## 🏗 Estrutura do Projeto

```
.
├── .gitignore
├── src
│   ├── main.py
│   ├── requirements.txt
│   ├── data
│   │   ├── Input
│   │   │   └── LATTES_INPUT_example.csv
│   │   ├── Logs
│   │   │   └── log 23-12-2025.log
│   │   ├── Output
│   │   └── Temp
│   │       └── NOMES_PROCESSADOS.txt
│   └── pacotes
│       ├── extracao
│       │   ├── acessarLattes.py
│       │   ├── extracaoDadosCurriculo.py
│       │   ├── extracaoDadosDiretorio.py
│       │   ├── extracaoDadosProducao.py
│       │   └── __init__.py
│       └── utils
│           ├── criar_pastas.py
│           ├── deletar_arquivos.py
│           ├── escrever_csv.py
│           ├── logs.py
│           ├── nomes_arquivos.py
│           ├── processados.py
│           └── __init__.py
```

---

## ▶️ Como Executar

### 1. Instale as dependências

```bash
pip install -r src/requirements.txt
```

### 2. Insira o arquivo de entrada

Coloque seu CSV contendo os nomes em:

```
src/data/Input/
```

Um arquivo exemplo já está incluído: `LATTES_INPUT_example.csv`.

### 3. Execute o projeto

```bash
python -m src.main
```

---

## 📁 Arquivos de Saída

Os resultados serão gerados em:

```
src/data/Output/
```

O arquivo:

```
src/data/Temp/NOMES_PROCESSADOS.txt
```

registra quais nomes já foram processados, permitindo execuções contínuas.

---

## 🧪 Testes

O projeto já contém um arquivo de input exemplo em:

```
src/data/Input/LATTES_INPUT_example.csv
```

---

## 🛠 Tecnologias Utilizadas

- Python  
- Multiprocessing  
- Automação/RPA  
- Manipulação de arquivos CSV  
- Logging estruturado  

---

## 👨‍💻 Autor

Projeto desenvolvido por **Tiago Henrique Freire de Oliveira Lopes**.  
Período de desenvolvimento: **3–4 semanas**.

---

## 📜 Licença

Licença: MIT (ou qualquer outra que deseje adicionar).

