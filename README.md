# Automação de Prontuários

Aplicação web desenvolvida em Python para automatizar o processamento de documentos admissionais, utilizando OCR para extrair informações de PDFs e gerar documentos Word a partir de modelos predefinidos.

## Sobre o Projeto

O projeto busca reduzir tarefas manuais no preenchimento de prontuários de funcionários, tornando o processo mais organizado e eficiente.

A aplicação permite enviar documentos digitalizados, extrair dados automaticamente, revisar as informações identificadas e gerar documentos preenchidos.

## Funcionalidades

- **Processamento de PDFs:** leitura de documentos digitalizados.
- **Extração de dados com OCR:** identificação de nome, data de admissão, cargo e unidade de trabalho.
- **Revisão de informações:** visualização e correção dos dados extraídos.
- **Integração com Excel:** armazenamento e atualização dos registros.
- **Geração de documentos:** preenchimento automatizado de capas de prontuários e declarações de alimentação em Word.
- **Relatórios:** registro dos resultados do processamento.
- **Interface web:** gerenciamento do fluxo por meio de uma aplicação Flask.

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python | Lógica e automação |
| Flask | Aplicação web |
| Tesseract OCR | Reconhecimento de texto |
| pytesseract | Integração entre Python e OCR |
| OpenPyXL | Manipulação de planilhas Excel |
| Microsoft Word | Geração de documentos |
| pywin32 | Automação do Word no Windows |
| Poppler | Processamento de PDFs |
| HTML, CSS e JavaScript | Interface web |
| JSON | Armazenamento de informações dos lotes |

## Fluxo de Funcionamento

1. Envio dos documentos PDF.
2. Extração automática das informações por OCR.
3. Revisão e correção dos dados identificados.
4. Validação dos campos obrigatórios.
5. Geração dos documentos Word.
6. Registro dos resultados do processamento.

## Requisitos

- Windows
- Python
- Microsoft Word instalado
- Tesseract OCR com suporte ao idioma português
- Poppler configurado
- Dependências Python do projeto

## Execução

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd automacao-prontuarios
```

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências, caso o arquivo `requirements.txt` esteja disponível:

```bash
python -m pip install -r requirements.txt
```

Inicie a aplicação:

```bash
python app.py
```

**Nota:** configure os caminhos do Tesseract e do Poppler conforme o ambiente de instalação. A execução também depende dos modelos Word e dos arquivos de configuração necessários.

## Segurança

Os documentos processados podem conter dados pessoais. Utilize informações fictícias em demonstrações e evite publicar PDFs, planilhas ou documentos reais de funcionários no repositório.

## Status

🚧 **Projeto em desenvolvimento.**

## Autor

**Vinicius Rodrigo**

Estudante de Engenharia de Software, interessado em desenvolvimento de software, Python e automação de processos.

- GitHub: [Perfil do GitHub](https://github.com/viniciusrodrigo-dev)
- LinkedIn: [Perfil do LinkedIn](https://www.linkedin.com/in/vini-silva-dev/)