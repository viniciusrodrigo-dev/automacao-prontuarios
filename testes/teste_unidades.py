from src.unidades import identificar_unidade

textos_teste = [
    "CAE MULHERES - BUTANTÃ, São Paulo - SP.",
    "CAEI SITIO DAS ALAMEDAS, São Paulo. SP.",
    "CA Jabaquara",
    "CA Jabaquara I",
    "CA Jabaquara II",
    "CA Jabaquara 1",
    "CA Jabaquara 2",
    "SAICA VILA SÔNIA, São Paulo - SP.",
    "UNIDADE DESCONHECIDA",
    "SAICA ABECAL JABAQUARA"
]

for texto in textos_teste:
    resultado = identificar_unidade(texto)

    print(f"Texto original: {texto}")
    print(f"Unidade identificada: {resultado}")
    print("-" * 50)