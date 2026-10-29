import re
from datetime import datetime
from .unidades import identificar_unidade


def extrair_dados(texto):
    """
    Recebe o texto extraído pelo OCR e identifica
    nome, data de admissão, cargo e unidade.
    """

    dados = {
        "nome": "",
        "data_admissao": "",
        "cargo": "",
        "unidade_original": "",
        "projeto": "",
        "data_demissao": ""
    }

    # Normaliza quebras de linha e espaços
    linhas = [
        linha.strip()
        for linha in texto.splitlines()
        if linha.strip()
    ]
    nome_encontrado = False

    for indice, linha in enumerate(linhas):

        linha_minuscula = linha.lower()

        # -----------------------------
        # NOME
        # -----------------------------

        if "nome do candidato selecionado:" in linha_minuscula:
            dados["nome"] = linha.split(":", 1)[1].strip()
            nome_encontrado = True

        elif linha_minuscula.startswith("nome:"):
            dados["nome"] = linha.split(":", 1)[1].strip()
            nome_encontrado = True

        # Novo modelo: "INFORMAÇÕES: NOME COMPLETO".
        # A regra só é aplicada quando a linha contém esse rótulo.
        elif re.match(r"^informa\w*\s*:\s*.+$", linha_minuscula):
            nome = linha.split(":", 1)[1].strip()
            if nome:
                dados["nome"] = nome
                nome_encontrado = True

        # -----------------------------
        # DATA DE ADMISSÃO
        # -----------------------------

        elif "data de admissão:" in linha_minuscula:
            valor = linha.split(":", 1)[1].strip()

            # Corrige espaços e confusão comum entre O e 0
            valor = valor.replace(" ", "")
            valor = re.sub(r"^[Oo](?=\d)", "0", valor)

            # Aceita dia e mês com um ou dois dígitos
            resultado = re.search(
                r"(\d{1,2})/(\d{1,2})/(\d{4})",
                valor
            )

            if resultado:
                dia, mes, ano = resultado.groups()

                try:
                    data = datetime(
                        int(ano),
                        int(mes),
                        int(dia)
                    )

                    dados["data_admissao"] = data.strftime(
                        "%d/%m/%Y"
                    )

                except ValueError:
                    dados["data_admissao"] = ""

        # -----------------------------
        # CARGO
        # -----------------------------

        elif linha_minuscula.startswith("cargo:"):
            dados["cargo"] = linha.split(":", 1)[1].strip()

        # -----------------------------
        # UNIDADE
        # -----------------------------

        elif "unidade do serviço:" in linha_minuscula:
            unidade_original = linha.split(":", 1)[1].strip()

            dados["unidade_original"] = unidade_original
            dados["projeto"] = identificar_unidade(unidade_original)

    return dados


# ---------------------------------
# TESTES COM OS EXEMPLOS FORNECIDOS
# ---------------------------------

modelo_1 = """
Nome do candidato selecionado: Gilmara Sousa Silva
Data de Admissão: 04/11/2026
Cargo: Agente Operacional — Cozinha
Unidade do serviço: CAE MULHERES - BUTANTÃ, São Paulo - SP.
"""

modelo_2 = """
MARCIA ANTONIA PRADO DA SILVA
Data de Admissão: O 4 /11/2026
Cargo: OPERACIONAL LIMPEZA
Unidade do serviço: CAEI SITIO DAS ALAMEDAS, São Paulo. SP.
"""

modelo_3 = """
Nome: Isael Felipe da Silva Santos
Data de Admissão: 05/11/2026
Cargo: Agente Operacional
Unidade do serviço: CA Jabaquara
"""


for numero, modelo in enumerate(
    [modelo_1, modelo_2, modelo_3],
    start=1
):
    print(f"\n--- MODELO {numero} ---")

    dados = extrair_dados(modelo)

    for campo, valor in dados.items():
        print(f"{campo}: {valor}")