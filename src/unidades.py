UNIDADES_OFICIAIS = [
    "CA AEROPORTO",
    "CA JABAQUARA I",
    "CA JABAQUARA II",
    "CA SÃO LEOPOLDO",
    "CAE MULHERES",
    "CAE FAMILIA",
    "CAEI 21",
    "CAEI SITIO",
    "CDI",
    "CTA BUTANTÃ",
    "CTA SANTO AMARO",
    "SAICA VILA SÔNIA",
    "SAICA CAPELA",
    "SAICA CIDADE ADEMAR",
    "SAICA IPIRANGA",
    "SAICA JABAQUARA",
    "SAICA SANTO AMARO",
    "VILA REECONTRO SANTO AMARO",
    "VILA REECONTRO SÃO MATHEUS"
]

import re
import unicodedata


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    texto = texto.upper()
    texto = re.sub(r"[^A-Z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def identificar_unidade(texto):
    texto_normalizado = normalizar_texto(texto)

    # Corrige variações de escrita de CA SÃO LEOPOLDO
    texto_normalizado = re.sub(
        r"\bC\s*A\s+SAO\s+LEOPOLDO\b",
        "CA SAO LEOPOLDO",
        texto_normalizado
    )

        # Corrige variação de SAICA JABAQUARA
    if "SAICA ABECAL JABAQUARA" in texto_normalizado:
        texto_normalizado = texto_normalizado.replace(
            "SAICA ABECAL JABAQUARA",
            "SAICA JABAQUARA"
        )

    # Regra específica para CA JABAQUARA
    if re.match(r"^CA JABAQUARA(?:\s|$)", texto_normalizado):
        restante = texto_normalizado[len("CA JABAQUARA"):].strip()

        if restante in ("", "1", "I"):
            return "CA JABAQUARA I"

        if restante in ("2", "II"):
            return "CA JABAQUARA II"

    # Reconhecimento das demais unidades oficiais
    correspondencias = []

    for unidade in UNIDADES_OFICIAIS:
        unidade_normalizada = normalizar_texto(unidade)

        if texto_normalizado.startswith(unidade_normalizada):
            correspondencias.append(unidade)

    if correspondencias:
        return max(correspondencias, key=len)

    return None