from pathlib import Path
from pypdf import PdfReader

pasta = Path(__file__).resolve().parent / "entrada"

arquivos = list(pasta.glob("*.pdf"))

if not arquivos:
    print("Nenhum PDF encontrado na pasta entrada.")
else:
    arquivo = arquivos[0]
    leitor = PdfReader(str(arquivo))

    texto_total = ""

    for pagina in leitor.pages:
        texto_total += pagina.extract_text() or ""

    if texto_total.strip():
        print("O PDF contém texto extraível!")
        print("\nPrimeiros 1000 caracteres:")
        print(texto_total[:1000])
    else:
        print("Nenhum texto extraível encontrado.")
        print("Pode ser necessário utilizar OCR.")