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
def categoria_mas_vista(matriz_usuarios, programas):
    """Devuelve la categoria mas vista entre todos los usuarios."""
    nombres, cantidades = contar_categorias_vistas(matriz_usuarios, programas)
    return mejor_de(nombres, cantidades)


# CANALES
def contar_canales_suscriptos(matriz_usuarios, canales_validos):
    """Cuenta cuantos usuarios estan suscriptos a cada canal.
    Devuelve dos listas paralelas: nombres de canal y cantidades."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        indice = u[CANAL_SUSCRIPTO]
        if 0 <= indice < len(canales_validos):
            canal = canales_validos[indice].upper()
            sumar_uno(nombres, cantidades, canal)
    return nombres, cantidades


def canal_mas_visto(matriz_usuarios, canales_validos):
    """Devuelve el canal con mas usuarios suscriptos."""
    nombres, cantidades = contar_canales_suscriptos(matriz_usuarios, canales_validos)
    return mejor_de(nombres, cantidades)


# HORARIOS
def contar_horarios(matriz_usuarios):
    """Cuenta cuantas veces aparece cada horario entre todos los usuarios.
    Devuelve dos listas paralelas: horarios y cantidades."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        for horario in u[HORARIOS]:
            sumar_uno(nombres, cantidades, horario)
    return nombres, cantidades


def horario_pico(matriz_usuarios):
    """Devuelve el horario en que mas usuarios suelen ver contenido."""
    nombres, cantidades = contar_horarios(matriz_usuarios)
    return mejor_de(nombres, cantidades)


def streamer_con_pico_de_vistas(matriz_usuarios, programas):
    """Devuelve el streamer favorito mejor posicionado entre los programas
    que se emiten justo en el horario pico (el streamer 'de moda' en el
    horario de mayor audiencia)."""
    pico = horario_pico(matriz_usuarios)
    if pico is None:
        return None

    nombres_streamers, cantidades_streamers = contar_streamers_favoritos(matriz_usuarios, programas)

    mejor_streamer = None
    mejor_cantidad = -1
    for p in programas:
        if p[HORARIO] == pico:
            streamer = p[STREAMER]
            cantidad = buscar_cantidad(nombres_streamers, cantidades_streamers, streamer)
            if cantidad > mejor_cantidad:
                mejor_cantidad = cantidad
                mejor_streamer = streamer
    return mejor_streamer

#REPORTE COMPLETO (para la opcion de administrador)
def imprimir_estadisticas(matriz_usuarios, programas, canales_validos):
    """Imprime en pantalla el resumen que pide la tarjeta de administrador:
    vistas de la gente, categorias mas vistas, streamer mas visto,
    streamer con pico de vistas y horario pico."""
    print("=== ESTADISTICAS DE VISTAS ===")
    print("Total de usuarios registrados: " + str(len(matriz_usuarios)))
    print("Canal mas visto (suscripto): " + str(canal_mas_visto(matriz_usuarios, canales_validos)))
    print("Categoria mas vista: " + str(categoria_mas_vista(matriz_usuarios, programas)))
    print("Streamer mas visto: " + str(streamer_mas_visto(matriz_usuarios, programas)))
    print("Streamer con pico de vistas: " + str(streamer_con_pico_de_vistas(matriz_usuarios, programas)))
    print("Horario pico: " + str(horario_pico(matriz_usuarios)))

    print("")
    print("--- Detalle: conteo por categoria ---")
    nombres_cat, cantidades_cat = contar_categorias_vistas(matriz_usuarios, programas)
    for i in range(len(nombres_cat)):
        print("  " + nombres_cat[i] + ": " + str(cantidades_cat[i]))

    print("")
    print("--- Detalle: conteo por streamer ---")
    nombres_str, cantidades_str = contar_streamers_favoritos(matriz_usuarios, programas)
    for i in range(len(nombres_str)):
        print("  " + nombres_str[i] + ": " + str(cantidades_str[i]))

    print("")
    print("--- Detalle: conteo por canal suscripto ---")
    nombres_can, cantidades_can = contar_canales_suscriptos(matriz_usuarios, canales_validos)
    for i in range(len(nombres_can)):
        print("  " + nombres_can[i] + ": " + str(cantidades_can[i]))

    print("")
    print("--- Detalle: conteo por horario ---")
    nombres_hor, cantidades_hor = contar_horarios(matriz_usuarios)
    for i in range(len(nombres_hor)):
        print("  " + nombres_hor[i] + ": " + str(cantidades_hor[i]))


#DEMOSTRACIÓN
if __name__ == "__main__":
    imprimir_estadisticas(matriz, programas, CANALES_VALIDOS)
