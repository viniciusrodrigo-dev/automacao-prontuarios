import re
import win32com.client
from pathlib import Path


MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]


def data_por_extenso(data_admissao):
    """Converte DD/MM/AAAA para o formato usado na declaração."""
    try:
        dia, mes, ano = data_admissao.split("/")
        dia_num = int(dia)
        mes_num = int(mes)
        if not 1 <= mes_num <= 12:
            raise ValueError
        return f"{dia_num:02d} de {MESES[mes_num - 1]} de {ano}"
    except (ValueError, AttributeError):
        raise ValueError(
            f"Data de admissão inválida: {data_admissao!r}. Use DD/MM/AAAA."
        )


def preencher_declaracao(dados):
    pasta_projeto = Path(__file__).resolve().parent.parent
    caminho_modelo = pasta_projeto / "modelos" / "declaracao_refeicao.docx"
    pasta_saida = pasta_projeto / "saida"

    campos_obrigatorios = ["nome", "data_admissao", "cargo", "projeto"]
    pendencias = [
        campo for campo in campos_obrigatorios
        if not str(dados.get(campo, "") or "").strip()
    ]
    if pendencias:
        print("Declaração não criada. Dados ausentes: " + ", ".join(pendencias))
        return False

    try:
        dia, mes, ano = dados["data_admissao"].split("/")
        nome_pasta = f"{dia}-{mes}"
        data_extenso = data_por_extenso(dados["data_admissao"])
    except ValueError as erro:
        print(f"Declaração não criada: {erro}")
        return False

    pasta_destino = pasta_saida / nome_pasta
    pasta_destino.mkdir(parents=True, exist_ok=True)

    nome_funcionario = str(dados["nome"]).strip()
    nome_arquivo = re.sub(r'[<>:"/\\|?*]', "", nome_funcionario)
    nome_arquivo = re.sub(r"\s+", "_", nome_arquivo).strip("._ ")

    if not nome_arquivo:
        print("Nome de arquivo inválido. Declaração não criada.")
        return False
    if not caminho_modelo.exists():
        print(f"Modelo da declaração não encontrado: {caminho_modelo}")
        print("Coloque declaracao_refeicao.docx dentro da pasta modelos do projeto.")
        return False

    caminho_saida = pasta_destino / f"{nome_arquivo}_Declaracao_Alimentacao.docx"
    if caminho_saida.exists():
        print(f"Declaração já existe. Não foi sobrescrita: {caminho_saida}")
        return False

    word = None
    documento = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        documento = word.Documents.Open(
            FileName=str(caminho_modelo),
            ConfirmConversions=False,
            ReadOnly=True,
            AddToRecentFiles=False
        )

        # Preencher a data procurando apenas "São Paulo,".
        # Assim, a busca não depende do ponto final, dos espaços ou de outros
        # caracteres que possam existir no modelo Word.
        data_preenchida = False

        for paragrafo in documento.Paragraphs:
            intervalo_paragrafo = paragrafo.Range.Duplicate
            busca_data = intervalo_paragrafo.Find
            busca_data.ClearFormatting()
            busca_data.Text = "São Paulo,"
            busca_data.Forward = True
            busca_data.Wrap = 0  # wdFindStop
            busca_data.Format = False

            if busca_data.Execute():
                intervalo_data = documento.Range(
                    busca_data.Parent.Start,
                    busca_data.Parent.End
                )
                intervalo_data.Collapse(0)  # wdCollapseEnd
                intervalo_data.InsertAfter(" " + data_extenso)
                data_preenchida = True
                break

        # Os demais campos são preenchidos procurando o parágrafo que contém
        # o rótulo, sem depender de espaços ou pontuação no final.
        campos = {
            "Nome:": str(dados["nome"]).strip(),
            "Serviço alocador:": str(dados["projeto"]).strip(),
            "Cargo:": str(dados["cargo"]).strip(),
        }

        for paragrafo in documento.Paragraphs:
            texto = paragrafo.Range.Text.strip()
            for marcador, valor in campos.items():
                if texto.startswith(marcador):
                    intervalo = documento.Range(
                        paragrafo.Range.Start,
                        paragrafo.Range.End - 1
                    )
                    intervalo.InsertAfter(" " + valor)
                    break

        if not data_preenchida:
            print(
                "Aviso: não encontrei 'São Paulo,' no modelo; "
                "a declaração será salva sem inserir a data."
            )

        documento.SaveAs2(FileName=str(caminho_saida), FileFormat=16)
        print(f"Declaração criada: {caminho_saida}")
        return True

    except Exception as erro:
        print(f"Erro ao criar declaração para {nome_funcionario}: {erro}")
        return False
    finally:
        if documento is not None:
            documento.Close(SaveChanges=False)
        if word is not None:
            word.Quit()