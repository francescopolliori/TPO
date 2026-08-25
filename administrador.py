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