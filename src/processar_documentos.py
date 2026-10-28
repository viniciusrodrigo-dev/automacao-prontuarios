from pathlib import Path
import json
import os
import pytesseract
from pdf2image import convert_from_path

from .extrair_dados import extrair_dados
from .relatorio import RelatorioProcessamento
from .planilha_revisao import PlanilhaRevisao

pasta_projeto = Path(__file__).resolve().parent.parent

pasta_entrada = Path(
    os.environ.get("pasta_entrada", str(pasta_projeto / "entrada"))
)

pasta_idiomas = pasta_projeto / "tessdata"
caminho_lote = Path(os.environ.get("caminho_lote", str(pasta_projeto / "lote_atual.json")))

relatorio = RelatorioProcessamento(pasta_projeto)
planilha_revisao = PlanilhaRevisao(pasta_projeto)
planilha_revisao.criar_planilha()

caminho_tesseract = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pasta_poppler = Path(
    r"C:\Users\Ana Beatriz\AppData\Local\Microsoft\WinGet\Packages"
    r"\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\poppler-25.07.0\Library\bin"
)
pytesseract.pytesseract.tesseract_cmd = str(caminho_tesseract)
os.environ["TESSDATA_PREFIX"] = str(pasta_idiomas)

arquivos_pdf = sorted(pasta_entrada.glob("*.pdf"))
if not arquivos_pdf:
    print("Nenhum PDF encontrado na pasta entrada.")
    print("O lote atual não foi alterado.")
    raise SystemExit(0)

# O manifesto guarda apenas os PDFs/páginas deste processamento.
# Os registros antigos continuam na planilha, mas não entram no lote atual.
itens_lote = []
print("\nINICIANDO LEITURA DOS DOCUMENTOS...\n")

for arquivo_pdf in arquivos_pdf:
    print(f"Processando: {arquivo_pdf.name}")
    try:
        paginas = convert_from_path(
            str(arquivo_pdf), dpi=300, poppler_path=str(pasta_poppler)
        )
    except Exception as erro:
        print(f"Erro ao abrir o PDF: {erro}")
        relatorio.registrar(
            arquivo_pdf=arquivo_pdf.name, pagina="", dados={},
            resultado="ERRO", detalhes=str(erro)
        )
        continue

    for numero, pagina in enumerate(paginas, start=1):
        dados = {}
        try:
            texto = pytesseract.image_to_string(pagina, lang="por")
            if texto.strip():
                dados = extrair_dados(texto)

            campos_obrigatorios = ["nome", "data_admissao", "cargo", "projeto"]
            pendencias = [campo for campo in campos_obrigatorios if not dados.get(campo)]

            planilha_revisao.registrar_funcionario(
                arquivo_pdf.name, numero, dados, pendencias
            )
            # Adiciona ao lote mesmo quando o registro já existia: isso permite
            # processar o lote atual sem duplicar nem sobrescrever correções.
            itens_lote.append({"arquivo_pdf": arquivo_pdf.name, "pagina": numero})

            if pendencias:
                resultado = "REVISAR"
                detalhes = "Campos ausentes: " + ", ".join(pendencias)
                print(f"  Página {numero}: precisa de revisão.")
            else:
                resultado = "AGUARDANDO GERAÇÃO"
                detalhes = "Dados extraídos para a planilha."
                print(f"  Página {numero}: dados extraídos.")

            relatorio.registrar(
                arquivo_pdf=arquivo_pdf.name, pagina=numero, dados=dados,
                resultado=resultado, pendencias=pendencias, detalhes=detalhes
            )
        except Exception as erro:
            print(f"  Erro na página {numero}: {erro}")
            relatorio.registrar(
                arquivo_pdf=arquivo_pdf.name, pagina=numero, dados=dados,
                resultado="ERRO", detalhes=str(erro)
            )

# Remove repetições e salva o lote. Se algum PDF falhou completamente, ele não
# será incluído; somente páginas lidas com sucesso entram no manifesto.
unicos = []
vistos = set()
for item in itens_lote:
    chave = (item["arquivo_pdf"], str(item["pagina"]))
    if chave not in vistos:
        vistos.add(chave)
        unicos.append(item)

caminho_lote.write_text(
    json.dumps(unicos, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nLEITURA CONCLUÍDA!")
print(f"Planilha de revisão: {planilha_revisao.caminho_arquivo}")
print(f"Relatório: {relatorio.caminho_arquivo}")
print(f"Lote atual salvo em: {caminho_lote}")
print(f"Páginas incluídas no lote atual: {len(unicos)}")
print("Revise os dados no Excel antes de gerar os documentos.")
