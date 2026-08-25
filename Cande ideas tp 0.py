
from zmq import STREAMER


programas = [
    [
        "Nadie Dice Nada",
        "Nicolas Occhiato",
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
        "Sone Que Volaba",
        "Migue Granados",
        "OLGA",
        "Lunes",
        "10:00",
        "Entretenimiento",
    ],
    [
        "Seria Increible",
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
        "Miercoles",
        "21:00",
        "Deporte",
    ],
    [
        "Y Que?",
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
        "Sabado",
        "17:00",
        "Espectaculo",
    ],
    [
        "Ibai Llanos",
        "Ibai",
        "TWITCH",
        "Sabado",
        "17:00",
        "Espectaculo",
    ],
]


print(
    f"{'Programa':<22}"
    f"{'Streamer':<22}"
    f"{'Canal':<15}"
    f"{'Dia':<14}"
    f"{'Horario':<10}"
    f"{'Categoria'}"
)

print("-" * 100)

for programa in programas:
    print(
        f"{programa[0]:<22}"
        f"{programa[1]:<22}"
        f"{programa[2]:<15}"
        f"{programa[3]:<14}"
        f"{programa[4]:<10}"
        f"{programa[5]}"
    )

#PROGRAMAS A AGREGAE
    [
        "Estación Junior",
        "Rulo",
        "GELATINA",
        "Sabado",
        "11:00",
        "Infantil",
    ],
    [
        "PlanetaKids",
        "Toy Zamora",
        "TWITCH",
        "Domingo",
        "12:00",
        "Infantil",
    ]


#fUNCIONES
def agregar_programa(programas,nombre,streamer,canal, dia, horario, categoria):
    programas.append([nombre,streamer,canal,dia,horario,categoria])
    return programas 




