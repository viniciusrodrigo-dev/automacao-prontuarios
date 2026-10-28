import re
import win32com.client
from pathlib import Path

def preencher_capa(dados):
    # ==========================================
    # 1. CAMINHOS DO PROJETO
    # ==========================================

    pasta_projeto = Path(__file__).resolve().parent.parent
    caminho_modelo = pasta_projeto / "modelos" / "capa_prontuario.docx"
    pasta_saida = pasta_projeto / "saida"

    # ==========================================
    # 2. VALIDAR DADOS OBRIGATÓRIOS
    # ==========================================

    campos_obrigatorios = [
        "nome",
        "data_admissao",
        "cargo",
        "projeto"
    ]

    pendencias = [
        campo
        for campo in campos_obrigatorios
        if not dados.get(campo)
    ]

    if pendencias:
        print(
            "Capa não criada. Dados ausentes: "
            + ", ".join(pendencias)
        )
        return False

    # ==========================================
    # 3. ORGANIZAR A PASTA DE SAÍDA
    # ==========================================

    data_admissao = dados["data_admissao"]

    try:
        dia, mes, ano = data_admissao.split("/")
        nome_pasta = f"{dia}-{mes}"
    except ValueError:
        print("Data de admissão inválida. Capa não criada.")
        return False

    pasta_destino = pasta_saida / nome_pasta
    pasta_destino.mkdir(parents=True, exist_ok=True)

    # ==========================================
    # 4. CRIAR NOME SEGURO PARA O ARQUIVO
    # ==========================================

    nome_funcionario = dados["nome"].strip()

    nome_arquivo = re.sub(
        r'[<>:"/\\|?*]',
        "",
        nome_funcionario
    )

    nome_arquivo = re.sub(r"\s+", "_", nome_arquivo)
    nome_arquivo = nome_arquivo.strip("._ ")

    if not nome_arquivo:
        print("Nome de arquivo inválido. Capa não criada.")
        return False

    caminho_saida = pasta_destino / f"{nome_arquivo}.docx"

    # Não sobrescrever capas existentes
    if caminho_saida.exists():
        print(f"Arquivo já existe. Capa não criada: {caminho_saida}")
        return False

    if not caminho_modelo.exists():
        print(f"Modelo Word não encontrado: {caminho_modelo}")
        return False

    # ==========================================
    # 5. PREPARAR DADOS DA CAPA
    # ==========================================

    campos = {
        "NOME:": dados["nome"],
        "DATA DE ADMISSÃO:": data_admissao,
        "PROJETO:": dados["projeto"],
        "CARGO:": dados["cargo"],
        "DATA DE DEMISSÃO:": ""
    }

    word = None
    documento = None

    try:
        # ==========================================
        # 6. ABRIR O WORD
        # ==========================================

        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False

        documento = word.Documents.Open(
            FileName=str(caminho_modelo),
            ConfirmConversions=False,
            ReadOnly=True,
            AddToRecentFiles=False
        )

        # ==========================================
        # 7. PREENCHER OS CAMPOS
        # ==========================================

        for paragrafo in documento.Paragraphs:
            texto = paragrafo.Range.Text.strip()

            if texto in campos:
                valor = campos[texto]

                if valor:
                    intervalo = documento.Range(
                        paragrafo.Range.Start,
                        paragrafo.Range.End - 1
                    )
                    intervalo.InsertAfter(" " + valor)

        # ==========================================
        # 8. MANTER DATA DE DEMISSÃO EM BRANCO
        # ==========================================

        paragrafo_demissao = None

        for paragrafo in documento.Paragraphs:
            if paragrafo.Range.Text.strip() == "DATA DE DEMISSÃO:":
                paragrafo_demissao = paragrafo
                break

        if paragrafo_demissao is not None:
            encontrou_demissao = False

            for paragrafo in documento.Paragraphs:
                if paragrafo.Range.Start == paragrafo_demissao.Range.Start:
                    encontrou_demissao = True
                    continue

                if encontrou_demissao:
                    if paragrafo.Range.Text.strip():
                        break

                    paragrafo.Range.Font.Size = 1
                    paragrafo.Format.SpaceBefore = 0
                    paragrafo.Format.SpaceAfter = 0

        # ==========================================
        # 9. SALVAR A CAPA
        # ==========================================

        documento.SaveAs2(
            FileName=str(caminho_saida),
            FileFormat=16
        )

        print(f"Capa criada: {caminho_saida}")
        return True

    except Exception as erro:
        print(f"Erro ao criar capa para {nome_funcionario}: {erro}")
        return False

    finally:
        if documento is not None:
            documento.Close(SaveChanges=False)

        if word is not None:
            word.Quit()