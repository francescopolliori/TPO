from listas_usuarios import matriz
from listas_programas import programas, CANALES_VALIDOS
from funciones_canales import STREAMER, CANAL, CATEGORIA, HORARIO

# Indices de la matriz de usuarios (ver listas_usuarios.py)
ID, NOMBRE_USUARIO, EDAD, CANAL_SUSCRIPTO, STREAMER_FAVORITO, HORARIOS = range(6)


#suma 1 a un valor dentro de dos listas paralelas 
def sumar_uno(nombres, cantidades, valor):
    """Busca `va en la lista `nombres`; si esta, le suma 1 a su cantidad
    en la misma posicion. Si no esta, lo agrega con cantidad 1."""
    encontrado = False
    for i in range(len(nombres)):
        if nombres[i] == valor:
            cantidades[i] = cantidades[i] + 1
            encontrado = True
    if not encontrado:
        nombres.append(valor)
        cantidades.append(1)

def buscar_cantidad(nombres, cantidades, valor):
    """Devuelve la cantidad asociada a `valor`, o 0 si no esta en la lista."""
    for i in range(len(nombres)):
        if nombres[i] == valor:
            return cantidades[i]
    return 0


def mejor_de(nombres, cantidades):
    """Devuelve el nombre con mayor cantidad de las dos listas paralelas,
    o None si estan vacias."""
    mejor_nombre = None
    mejor_cantidad = 0
    for i in range(len(nombres)):
        if cantidades[i] > mejor_cantidad:
            mejor_cantidad = cantidades[i]
            mejor_nombre = nombres[i]
    return mejor_nombre


# STREAMERS
def contar_streamers_favoritos(matriz_usuarios, programas):
    """Cuenta cuantos usuarios tienen a cada streamer como favorito.
    Devuelve dos listas paralelas: nombres de streamer y cantidades."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        indice = u[STREAMER_FAVORITO]
        if 0 <= indice < len(programas):
            streamer = programas[indice][STREAMER]
            sumar_uno(nombres, cantidades, streamer)
    return nombres, cantidades


def streamer_mas_visto(matriz_usuarios, programas):
    """Devuelve el streamer favorito de la mayor cantidad de usuarios."""
    nombres, cantidades = contar_streamers_favoritos(matriz_usuarios, programas)
    return mejor_de(nombres, cantidades)


# CATEGORIAS
def contar_categorias_vistas(matriz_usuarios, programas):
    """Cuenta cuantos usuarios ven cada categoria (segun su streamer favorito).
    Devuelve dos listas paralelas: nombres de categoria y cantidades."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        indice = u[STREAMER_FAVORITO]
        if 0 <= indice < len(programas):
            categoria = programas[indice][CATEGORIA]
            sumar_uno(nombres, cantidades, categoria)
    return nombres, cantidades        