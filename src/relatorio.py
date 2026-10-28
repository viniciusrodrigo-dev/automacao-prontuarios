import csv
from datetime import datetime
from pathlib import Path


class RelatorioProcessamento:

    def __init__(self, pasta_projeto):
        self.pasta_relatorios = Path(pasta_projeto) / "relatorios"
        self.pasta_relatorios.mkdir(
            parents=True,
            exist_ok=True
        )

        data_hora = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        self.caminho_arquivo = (
            self.pasta_relatorios
            / f"relatorio_processamento_{data_hora}.csv"
        )

        self.colunas = [
            "data_hora",
            "arquivo_pdf",
            "pagina",
            "nome",
            "data_admissao",
            "cargo",
            "projeto",
            "resultado",
            "pendencias",
            "detalhes"
        ]

        with open(
            self.caminho_arquivo,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=self.colunas,
                delimiter=";"
            )
            escritor.writeheader()

    def registrar(
        self,
        arquivo_pdf,
        pagina,
        dados,
        resultado,
        pendencias=None,
        detalhes=""
    ):
        if pendencias is None:
            pendencias = []

        registro = {
            "data_hora": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            "arquivo_pdf": arquivo_pdf,
            "pagina": pagina,
            "nome": dados.get("nome", ""),
            "data_admissao": dados.get("data_admissao", ""),
            "cargo": dados.get("cargo", ""),
            "projeto": dados.get("projeto", ""),
            "resultado": resultado,
            "pendencias": ", ".join(pendencias),
            "detalhes": detalhes
        }

        with open(
            self.caminho_arquivo,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=self.colunas,
                delimiter=";"
            )
            escritor.writerow(registro)