from pathlib import Path
import os
import pytesseract
from pdf2image import convert_from_path


# ==========================================
# 1. CONFIGURAÇÕES DO PROJETO
# ==========================================

# Localiza a pasta principal do projeto
pasta_projeto = Path(__file__).resolve().parent

# Pasta que contém os PDFs digitalizados
pasta_entrada = pasta_projeto / "entrada"

# Pasta onde salvamos o idioma português
pasta_idiomas = pasta_projeto / "tessdata"

# Caminho do executável do Tesseract
caminho_tesseract = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Caminho dos executáveis do Poppler
pasta_poppler = Path(
    r"C:\Users\Ana Beatriz\AppData\Local\Microsoft\WinGet\Packages"
    r"\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\poppler-25.07.0\Library\bin"
)


# ==========================================
# 2. CONFIGURAÇÃO DO TESSERACT
# ==========================================

# Informa ao Python onde está o Tesseract
pytesseract.pytesseract.tesseract_cmd = str(caminho_tesseract)

# Define a pasta do idioma português
os.environ["TESSDATA_PREFIX"] = str(pasta_idiomas)


# ==========================================
# 3. VERIFICAÇÃO DOS ARQUIVOS
# ==========================================

if not caminho_tesseract.exists():
    raise FileNotFoundError(
        f"Tesseract não encontrado: {caminho_tesseract}"
    )

if not (pasta_idiomas / "por.traineddata").exists():
    raise FileNotFoundError(
        f"Idioma português não encontrado: "
        f"{pasta_idiomas / 'por.traineddata'}"
    )

if not pasta_poppler.exists():
    raise FileNotFoundError(
        f"Pasta do Poppler não encontrada: {pasta_poppler}"
    )


# ==========================================
# 4. LOCALIZAÇÃO DOS PDFs
# ==========================================

arquivos_pdf = sorted(pasta_entrada.glob("*.pdf"))

if not arquivos_pdf:
    print("Nenhum PDF encontrado na pasta entrada.")
    raise SystemExit(0)

# Seleciona o primeiro PDF encontrado
arquivo_pdf = arquivos_pdf[0]

print("=" * 50)
print("AUTOMAÇÃO DE LEITURA DE FORMULÁRIOS")
print("=" * 50)

print(f"\nArquivo selecionado: {arquivo_pdf.name}")
print("Convertendo PDF em imagens...")


# ==========================================
# 5. CONVERSÃO DO PDF EM IMAGENS
# ==========================================

paginas = convert_from_path(
    str(arquivo_pdf),
    dpi=300,
    poppler_path=str(pasta_poppler)
)

print(f"Total de páginas encontradas: {len(paginas)}")


# ==========================================
# 6. RECONHECIMENTO DE TEXTO (OCR)
# ==========================================

for numero, pagina in enumerate(paginas, start=1):

    print(f"\n{'=' * 20} PÁGINA {numero} {'=' * 20}")

    texto = pytesseract.image_to_string(
        pagina,
        lang="por",
    )

    if texto.strip():
        print(texto)
    else:
        print("Nenhum texto foi reconhecido nesta página.")


# ==========================================
# 7. FINALIZAÇÃO
# ==========================================

print("\n" + "=" * 50)
print("TESTE DE OCR CONCLUÍDO")
print("=" * 50)