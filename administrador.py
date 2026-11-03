import json

from funciones_canales import STREAMER, CATEGORIA, HORARIO

RUTA_USUARIOS = "lista_usuarios.json"
RUTA_LOG_MIGRACION = "migracion_log.txt"


ID, NOMBRE_USUARIO, EDAD, CANAL_SUSCRIPTO, STREAMER_FAVORITO, HORARIOS = range(6)


#  CARGA DESDE JSON
def es_entero(valor):
    """Valida si es un int real usando excepciones. Devuelve false para bools"""
    if type(valor) == bool:
        return False
    try:
        entero = int(valor)

        if type(valor) == int:
            return True
        return False
    except (ValueError, TypeError):
        return False


def cargar_usuarios(ruta):
    """Devuelve la matriz de usuarios guardada en el JSON.
    Si el archivo no existe devuelve una matriz vacía.
    Lanza ValueError si el JSON está dañado o tiene un formato inválido."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lista = json.load(archivo)["usuarios"]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError):
        raise ValueError(f"el archivo '{ruta}' está dañado o tiene un formato inválido.")

    if type(lista) != list:
        raise ValueError(f"el archivo '{ruta}' está dañado o tiene un formato inválido.")

    for u in lista:
        valido = (type(u) == list and len(u) == 6
                  and es_entero(u[ID]) and es_entero(u[EDAD])
                  and type(u[NOMBRE_USUARIO]) == str
                  and type(u[CANAL_SUSCRIPTO]) == str
                  and type(u[STREAMER_FAVORITO]) == str
                  and type(u[HORARIOS]) == list
                  and all(type(h) == str for h in u[HORARIOS]))
        if not valido:
            raise ValueError(f"'{ruta}' tiene un usuario con formato inválido: {u}")
    return lista


def guardar_usuarios(ruta, matriz_usuarios):
    """Guarda la matriz de usuarios en el JSON ({"usuarios": [...]}).
    Lanza OSError si no se puede escribir el archivo."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump({"usuarios": matriz_usuarios}, archivo, ensure_ascii=False, indent=4)


#  AUXILIARES
def sumar_uno(nombres, cantidades, valor):
    """Busca `valor` en la lista `nombres`; si está, le suma 1 a su cantidad
    en la misma posición. Si no está, lo agrega con cantidad 1."""
    encontrado = False
    for i in range(len(nombres)):
        if nombres[i] == valor:
            cantidades[i] = cantidades[i] + 1
            encontrado = True
    if not encontrado:
        nombres.append(valor)
        cantidades.append(1)


def buscar_cantidad(nombres, cantidades, valor):
    """Devuelve la cantidad asociada a `valor`, o 0 si no está en la lista."""
    for i in range(len(nombres)):
        if nombres[i] == valor:
            return cantidades[i]
    return 0


def mejor_de(nombres, cantidades):
    """Devuelve el nombre con mayor cantidad de las dos listas paralelas,
    o None si están vacías."""
    mejor_nombre = None
    mejor_cantidad = 0
    for i in range(len(nombres)):
        if cantidades[i] > mejor_cantidad:
            mejor_cantidad = cantidades[i]
            mejor_nombre = nombres[i]
    return mejor_nombre


def buscar_programa_de_streamer(programas, streamer):
    """Devuelve el primer programa de ese streamer (ignora mayúsculas y
    espacios de más) o None si ya no existe en programas."""
    clave = " ".join(streamer.split()).lower()
    for p in programas:
        if " ".join(p[STREAMER].split()).lower() == clave:
            return p
    return None


def normalizar_canal(canal):
    """Mismo criterio que usa el set de canales de abm_programas."""
    return " ".join(canal.split()).lower()


# STREAMERS
def contar_streamers_favoritos(matriz_usuarios, programas):
    """Cuenta cuántos usuarios tienen a cada streamer como favorito (solo los
    que todavía tienen programas). Devuelve dos listas paralelas."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        p = buscar_programa_de_streamer(programas, u[STREAMER_FAVORITO])
        if p is not None:
            sumar_uno(nombres, cantidades, p[STREAMER])
    return nombres, cantidades


def streamer_mas_visto(matriz_usuarios, programas):
    """Devuelve el streamer favorito de la mayor cantidad de usuarios."""
    nombres, cantidades = contar_streamers_favoritos(matriz_usuarios, programas)
    return mejor_de(nombres, cantidades)


# CATEGORIAS
def contar_categorias_vistas(matriz_usuarios, programas):
    """Cuenta cuántos usuarios ven cada categoría (según su streamer favorito).
    Devuelve dos listas paralelas."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        p = buscar_programa_de_streamer(programas, u[STREAMER_FAVORITO])
        if p is not None:
            sumar_uno(nombres, cantidades, p[CATEGORIA])
    return nombres, cantidades


def categoria_mas_vista(matriz_usuarios, programas):
    """Devuelve la categoría más vista entre todos los usuarios."""
    nombres, cantidades = contar_categorias_vistas(matriz_usuarios, programas)
    return mejor_de(nombres, cantidades)


# CANALES
def contar_canales_suscriptos(matriz_usuarios, canales):
    """Cuenta cuántos usuarios están suscriptos a cada canal. 'canales' es el
    set de canales existentes: se ignoran suscripciones a canales que ya no
    existen. Devuelve dos listas paralelas."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        canal = normalizar_canal(u[CANAL_SUSCRIPTO])
        if canal in canales:
            sumar_uno(nombres, cantidades, canal.upper())
    return nombres, cantidades


def canal_mas_visto(matriz_usuarios, canales):
    """Devuelve el canal con más usuarios suscriptos."""
    nombres, cantidades = contar_canales_suscriptos(matriz_usuarios, canales)
    return mejor_de(nombres, cantidades)


# HORARIOS
def contar_horarios(matriz_usuarios):
    """Cuenta cuántas veces aparece cada horario entre todos los usuarios.
    Devuelve dos listas paralelas."""
    nombres = []
    cantidades = []
    for u in matriz_usuarios:
        for horario in u[HORARIOS]:
            sumar_uno(nombres, cantidades, horario)
    return nombres, cantidades


def horario_pico(matriz_usuarios):
    """Devuelve el horario en que más usuarios suelen ver contenido."""
    nombres, cantidades = contar_horarios(matriz_usuarios)
    return mejor_de(nombres, cantidades)


def streamer_con_pico_de_vistas(matriz_usuarios, programas):
    """Devuelve el streamer favorito mejor posicionado entre los programas
    que se emiten justo en el horario pico."""
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


# TABLA
def mostrar_tabla_usuarios(matriz_usuarios, programas, canales):
    """Imprime una tabla alineada con los datos de los usuarios. Si el canal o
    el streamer de un usuario ya no existen, muestra 'Sin Suscripción' / 'Ninguno'."""
    w_id, w_nom, w_edad, w_canal, w_streamer, w_hor = 4, 12, 6, 18, 18, 20

    linea = (f"+{'-'*(w_id+2)}+{'-'*(w_nom+2)}+{'-'*(w_edad+2)}+{'-'*(w_canal+2)}"
             f"+{'-'*(w_streamer+2)}+{'-'*(w_hor+2)}+")

    print(linea)
    print(f"| {'ID':<{w_id}} | {'Nombre':<{w_nom}} | {'Edad':<{w_edad}} | {'Canal Sub':<{w_canal}} "
          f"| {'Streamer Fav.':<{w_streamer}} | {'Horarios':<{w_hor}} |")
    print(linea)

    for u in matriz_usuarios:
        canal_u = normalizar_canal(u[CANAL_SUSCRIPTO])
        canal = canal_u.upper() if canal_u in canales else "Sin Suscripción"

        p = buscar_programa_de_streamer(programas, u[STREAMER_FAVORITO])
        streamer = p[STREAMER] if p is not None else "Ninguno"

        horarios = ", ".join(u[HORARIOS])
        print(f"| {u[ID]:<{w_id}} | {u[NOMBRE_USUARIO]:<{w_nom}} | {u[EDAD]:<{w_edad}} "
              f"| {canal:<{w_canal}} | {streamer:<{w_streamer}} | {horarios:<{w_hor}} |")

    print(linea)


#  REPORTE COMPLETO
def imprimir_detalle(titulo, nombres, cantidades):
    """Imprime un conteo (dos listas paralelas) con un título."""
    print("")
    print("--- Detalle: " + titulo + " ---")
    for i in range(len(nombres)):
        print("  " + nombres[i] + ": " + str(cantidades[i]))


def imprimir_estadisticas(matriz_usuarios, programas, canales):
    """Resumen para la opción de administrador."""
    print("=== ESTADISTICAS DE VISTAS ===")
    print("Total de usuarios registrados: " + str(len(matriz_usuarios)))
    print("Canal mas visto (suscripto): " + str(canal_mas_visto(matriz_usuarios, canales)))
    print("Categoria mas vista: " + str(categoria_mas_vista(matriz_usuarios, programas)))
    print("Streamer mas visto: " + str(streamer_mas_visto(matriz_usuarios, programas)))
    print("Streamer con pico de vistas: " + str(streamer_con_pico_de_vistas(matriz_usuarios, programas)))
    print("Horario pico: " + str(horario_pico(matriz_usuarios)))

    imprimir_detalle("conteo por categoria", *contar_categorias_vistas(matriz_usuarios, programas))
    imprimir_detalle("conteo por streamer", *contar_streamers_favoritos(matriz_usuarios, programas))
    imprimir_detalle("conteo por canal suscripto", *contar_canales_suscriptos(matriz_usuarios, canales))
    imprimir_detalle("conteo por horario", *contar_horarios(matriz_usuarios))

    print("")
    mostrar_tabla_usuarios(matriz_usuarios, programas, canales)


#  MIGRACIÓN (formato viejo con índices -> formato nuevo con nombres)
# Tupla: la correspondencia índice -> canal del sistema viejo es fija y no se modifica.
CANALES_ANTIGUOS = ("luzu tv", "olga", "vorterix", "gelatina", "kick", "twitch")
STREAMER_EN_PROGRAMA_VIEJO = 1   # posición del streamer dentro de un programa viejo


def convertir_usuario(u, programas_viejos):
    """Convierte un usuario viejo (con índices) al formato nuevo.
    Devuelve una tupla (usuario_nuevo, problemas): 'problemas' es la lista de
    textos con lo que no se pudo convertir (índices inexistentes o inválidos)."""
    problemas = []
    i_canal, i_streamer = u[CANAL_SUSCRIPTO], u[STREAMER_FAVORITO]

    if es_entero(i_canal) and 0 <= i_canal < len(CANALES_ANTIGUOS):
        canal = CANALES_ANTIGUOS[i_canal]
    else:
        canal = ""
        problemas.append(f"canal inexistente (índice {i_canal})")

    if es_entero(i_streamer) and 0 <= i_streamer < len(programas_viejos):
        streamer = programas_viejos[i_streamer][STREAMER_EN_PROGRAMA_VIEJO]
    else:
        streamer = ""
        problemas.append(f"streamer inexistente (índice {i_streamer})")

    nuevo = [u[ID], u[NOMBRE_USUARIO], u[EDAD], canal, streamer, list(u[HORARIOS])]
    return nuevo, problemas


def convertir_usuarios(usuarios_viejos, programas_viejos):
    """Convierte la lista completa. Devuelve (convertidos, avisos):
    - convertidos: usuarios en formato nuevo, sin IDs repetidos.
    - avisos: diccionario {id_usuario: [problemas]} con lo que no se pudo convertir."""
    convertidos = []
    avisos = {}
    ids_vistos = set()   # el set evita migrar dos usuarios con el mismo ID
    for u in usuarios_viejos:
        if u[ID] in ids_vistos:
            avisos[u[ID]] = avisos.get(u[ID], []) + ["ID repetido, no se migró"]
            continue
        ids_vistos.add(u[ID])
        nuevo, problemas = convertir_usuario(u, programas_viejos)
        convertidos.append(nuevo)
        if problemas:
            avisos[u[ID]] = problemas
    return convertidos, avisos


# LOG DE MIGRACIÓN (archivo de texto: una línea por usuario con problemas)
def guardar_log_migracion(ruta, avisos):
    """Escribe una línea 'id;problema1 | problema2' por cada usuario con avisos.
    Lanza OSError si no se puede escribir el archivo."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        for id_usuario, problemas in avisos.items():
            archivo.write(f"{id_usuario};{' | '.join(problemas)}\n")


def leer_log_migracion(ruta):
    """Lee el log y devuelve un diccionario {id_usuario: [problemas]}.
    Si el archivo no existe devuelve {} (no hubo avisos). Ignora líneas inválidas."""
    avisos = {}
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                id_texto, _, resto = linea.strip().partition(";")
                if id_texto.isdigit():
                    avisos[int(id_texto)] = resto.split(" | ")
    except FileNotFoundError:
        return {}
    return avisos


def usuarios_a_revisar(matriz_usuarios, avisos):
    """Devuelve los usuarios que figuran en los avisos y siguen sin canal o sin streamer."""
    pendientes = []
    for u in matriz_usuarios:
        if u[ID] in avisos and (u[CANAL_SUSCRIPTO] == "" or u[STREAMER_FAVORITO] == ""):
            pendientes.append(u)
    return pendientes


def imprimir_usuarios_a_revisar(matriz_usuarios, ruta_log):
    """Muestra los usuarios del log de migración que todavía hay que corregir."""
    try:
        avisos = leer_log_migracion(ruta_log)
    except OSError as error:
        print("No se pudo leer el log de migración:", error)
        return
    pendientes = usuarios_a_revisar(matriz_usuarios, avisos)
    if not pendientes:
        print("No hay usuarios pendientes de revisión.")
        return
    print("=== USUARIOS A REVISAR ===")
    for u in pendientes:
        print(f"  ID {u[ID]} - {u[NOMBRE_USUARIO]}: {' | '.join(avisos[u[ID]])}")
