# Automação de Prontuários

Aplicação desenvolvida em Python para automatizar etapas do processamento de documentos de admissão de funcionários.

## Funcionalidades

- Leitura de PDFs digitalizados utilizando OCR.
- Extração de nome, data de admissão, cargo e unidade.
- Identificação de unidades por meio de uma lista oficial.
- Registro dos dados extraídos em planilha Excel para revisão.
- Identificação de campos pendentes.
- Geração automatizada de capas de prontuário e declarações em Word.
- Registro dos resultados do processamento.

## Tecnologias

- Python
- Tesseract OCR
- PyTesseract
- pdf2image
- Poppler
- Microsoft Word
- python-docx
- openpyxl

## Estrutura do projeto

- `src/`: código-fonte da aplicação.
- `ferramentas/`: scripts auxiliares.
- `modelos/`: modelos de documentos utilizados na geração.
- `entrada/`: PDFs utilizados no processamento local.
- `saida/`: documentos gerados.
- `relatorios/`: relatórios de processamento.
- `tessdata/`: arquivos de idioma utilizados pelo Tesseract.
- `testes/`: testes automatizados.

## Requisitos

- Python compatível com as dependências do projeto.
- Tesseract OCR instalado e configurado.
- Poppler instalado e configurado.
- Microsoft Word instalado para os recursos que utilizam automação do Word.

## Instalação

Clone o repositório e entre na pasta:

```bash
git clone URL_DO_REPOSITORIO
cd automacao-prontuarios
```

Crie e ative um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure os caminhos locais do Tesseract e do Poppler conforme as instruções do projeto.

## Execução

Os comandos de execução serão documentados após a consolidação da interface e dos pontos de entrada da aplicação.

## Privacidade

Este projeto pode processar documentos que contêm dados pessoais. Arquivos reais de funcionários, planilhas preenchidas e documentos gerados não devem ser publicados no repositório.

## Status

Projeto em desenvolvimento.