titulos=[
        "Nombre",
        "Streamer",
        "Canal",
        "Día",
        "Horario",
        "Categoría"
        ]

programas = [
    [
        "Nadie Dice Nada",
        "Nicolás Occhiato",
        "LUZU TV",
        "Lunes",
        "10:00",
        "Entretenimiento",
    ],
    [
        "Antes Que Nadie",
        "Diego Leuco",
        "LUZU TV",
        "Martes",
        "08:00",
        "Actualidad",
    ],
    [
        "Soñé Que Volaba",
        "Migue Granados",
        "OLGA",
        "Lunes",
        "10:00",
        "Entretenimiento",
    ],
    [
        "Sería Increíble",
        "Nati Jota",
        "OLGA",
        "Martes",
        "09:00",
        "Humor",
    ],
    [
        "Paren La Mano",
        "Luquitas Rodriguez",
        "VORTERIX",
        "Miércoles",
        "21:00",
        "Deporte",
    ],
    [
        "Y Qué?",
        "Guillermo Aquino",
        "VORTERIX",
        "Jueves",
        "10:00",
        "Humor",
    ],
    [
        "Industria Nacional",
        "Pedro Rosemblat",
        "GELATINA",
        "Viernes",
        "08:00",
        "Actualidad",
    ],
    [
        "412",
        "Davo Xeneize",
        "KICK",
        "Viernes",
        "21:00",
        "Deporte",
    ],
    [
        "La Faraona",
        "Martin Cirio",
        "TWITCH",
        "Sábado",
        "17:00",
        "Espectáculo",
    ],
    [
        "Ibai Llanos",
        "Ibai",
        "TWITCH",
        "Sábado",
        "17:00",
        "Espectáculo",
    ],
]


for programa in programas:
    print(
        f"{programa[0]} |"
        f"{programa[1]} |"
        f"{programa[2]} |"
        f"{programa[3]} |"
        f"{programa[4]} |"
        f"{programa[5]}")


def buscar_programa(programas, texto):
    """Busca programas donde el nombre o streamer coincida (sin
    importar mayúsculas/minúsculas) con el texto ingresado.
    Devuelve una lista con los programas encontrados."""
    texto = texto.strip().lower()
    resultados = []

    for programa in programas:
        nombre = programa[0].lower()
        streamer = programa[1].lower()

        if texto in nombre or texto in streamer:
            resultados.append(programa)


    return resultados