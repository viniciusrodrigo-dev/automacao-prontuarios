from pathlib import Path
from pypdf import PdfReader

# Localiza as pastas do projeto
pasta_projeto = Path(__file__).resolve().parent
pasta_entrada = pasta_projeto / "entrada"

# Localiza os arquivos PDF
arquivos_pdf = list(pasta_entrada.glob("*.pdf"))

if not arquivos_pdf:
    print("Nenhum PDF encontrado na pasta entrada.")
    raise SystemExit

# Por enquanto, lê somente o primeiro PDF
arquivo_pdf = arquivos_pdf[0]

print(f"Arquivo selecionado: {arquivo_pdf.name}")

# Abre o PDF e extrai o texto
leitor = PdfReader(str(arquivo_pdf))

texto_completo = []

for numero, pagina in enumerate(leitor.pages, start=1):
    texto = pagina.extract_text() or ""
    texto_completo.append(texto)

    print(f"\n--- Página {numero} ---")
    print(texto)

# Salva o texto extraído para facilitar a análise
caminho_texto = pasta_entrada / "texto_extraido.txt"

caminho_texto.write_text(
    "\n".join(texto_completo),
    encoding="utf-8"
)

print("\nLeitura concluída!")
print(f"Texto extraído salvo em: {caminho_texto}")