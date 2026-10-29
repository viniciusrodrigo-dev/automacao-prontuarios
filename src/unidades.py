import re
import unicodedata

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
    "VILA REECONTRO SÃO MATHEUS",
]


def normalizar_texto(texto):
    """Remove acentos e pontuação e padroniza espaços e maiúsculas."""
    texto = unicodedata.normalize("NFD", texto or "")
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    texto = texto.upper()
    texto = re.sub(r"[^A-Z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def identificar_unidade(texto):
    """
    Identifica uma unidade oficial mesmo quando aparece depois de um endereço
    ou acompanhada de termos como ABECAL e CAPELA DO SOCORRO.
    Retorna o nome oficial cadastrado ou None quando não há correspondência.
    """
    texto_normalizado = normalizar_texto(texto)
    if not texto_normalizado:
        return None

    # Corrige erros de OCR e variantes recorrentes sem alterar os nomes oficiais.
    texto_normalizado = re.sub(
        r"\bVILA\s+REENCONTRO\b",
        "VILA REECONTRO",
        texto_normalizado,
    )
    texto_normalizado = re.sub(
        r"\bC\s*A\s+SAO\s+LEOPOLDO\b",
        "CA SAO LEOPOLDO",
        texto_normalizado,
    )

    # Variações em que a unidade vem acompanhada do nome da organização.
    regras = [
        (r"\bSAICA\s+(?:ABECAL\s+)?VILA\s+SONIA(?:\s+ABECAL)?\b",
         "SAICA VILA SONIA"),
        (r"\bSAICA\s+(?:ABECAL\s+)?CAPELA(?:\s+DO\s+SOCORRO)?(?:\s+ABECAL)?\b",
         "SAICA CAPELA"),
        (r"\bSAICA\s+IPIRANGA(?:\s+ABECAL)?\b",
         "SAICA IPIRANGA"),
        (r"\bSAICA\s+ABECAL\s+JABAQUARA\b",
         "SAICA JABAQUARA"),
    ]
    for padrao, substituicao in regras:
        texto_normalizado = re.sub(padrao, substituicao, texto_normalizado)

    # Regra específica: CA JABAQUARA sem número significa CA JABAQUARA I.
    if re.match(r"^CA JABAQUARA(?:\s|$)", texto_normalizado):
        restante = texto_normalizado[len("CA JABAQUARA"):].strip()
        if restante in ("", "1", "I"):
            return "CA JABAQUARA I"
        if restante in ("2", "II"):
            return "CA JABAQUARA II"

    # Procurar em qualquer posição é necessário porque algumas fichas incluem
    # o endereço antes do nome da unidade.
    correspondencias = []
    for unidade in UNIDADES_OFICIAIS:
        unidade_normalizada = normalizar_texto(unidade)
        if re.search(r"\b" + re.escape(unidade_normalizada) + r"\b", texto_normalizado):
            correspondencias.append(unidade)

    if correspondencias:
        return max(correspondencias, key=len)

    return None
