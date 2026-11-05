import json


def cargar_json(ruta):
    """Carga un archivo JSON y devuelve su contenido como una lista de diccionarios."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'.")
        return []


def obtener_mejor(diccionario_conteo):
    """Busca y devuelve la clave con el valor más alto en un diccionario."""
    mejor_clave = "Ninguno"
    mejor_valor = 0
    for clave, valor in diccionario_conteo.items():
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_clave = clave
    return mejor_clave



def analizar_streamers(usuarios):
    """Analiza los streamers favoritos de los usuarios y devuelve el más popular junto con un conteo de todos."""
    conteo = {}
    for u in usuarios:
        streamer = u["streamer_favorito"]
        if streamer in conteo:
            conteo[streamer] += 1
        else:
            conteo[streamer] = 1
    return obtener_mejor(conteo), conteo

def analizar_categorias(usuarios, programas):
    """Analiza los géneros de los programas favoritos de los usuarios y devuelve el más popular junto con un conteo de todos."""
    conteo = {}
    for u in usuarios:
        streamer_fav = u["streamer_favorito"]
        
        # Buscamos qué género tiene el programa de este streamer
        categoria = "Sin género"
        for p in programas:
            if p["conductor"] == streamer_fav:
                categoria = p["genero"]
                break  # Lo encontramos, dejamos de buscar
        
        if categoria in conteo:
            conteo[categoria] += 1
        else:
            conteo[categoria] = 1
            
    return obtener_mejor(conteo), conteo

def analizar_canales(usuarios):
    """Analiza los canales a los que están suscritos los usuarios y devuelve el más popular junto con un conteo de todos."""
    conteo = {}
    for u in usuarios:
        canal = u["suscripcion"]
        if canal in conteo:
            conteo[canal] += 1
        else:
            conteo[canal] = 1
    return obtener_mejor(conteo), conteo

def analizar_horarios(usuarios):
    """Analiza los horarios recurrentes de los usuarios y devuelve el más popular junto con un conteo de todos."""
    conteo = {}
    for u in usuarios:
        for horario in u["horario_recurrentes"]:
            if horario in conteo:
                conteo[horario] += 1
            else:
                conteo[horario] = 1
    return obtener_mejor(conteo), conteo

def streamer_con_pico_de_vistas(usuarios, programas):
    """Determina qué streamer tiene el mayor número de usuarios que coinciden con el horario pico de visualización."""
    mejor_horario, _ = analizar_horarios(usuarios)
    if mejor_horario == "Ninguno":
        return "Ninguno"

    conteo = {}
    for u in usuarios:
        streamer_fav = u["streamer_favorito"]
        for p in programas:
            if p["conductor"] == streamer_fav and p["hora_inicio"] == mejor_horario:
                if streamer_fav in conteo:
                    conteo[streamer_fav] += 1
                else:
                    conteo[streamer_fav] = 1
                break

    return obtener_mejor(conteo)



def mostrar_tabla_usuarios(usuarios):
    """Imprime una tabla limpia con bordes y anchos fijos."""
    ancho = 110
    print("\n" + "=" * ancho)
    print(f"| {'ID':<4} | {'Nombre':<18} | {'Edad':<4} | {'Canal Sub':<20} | {'Streamer Fav.':<20} | {'Horarios':<25} |")
    print("-" * ancho)

    for u in usuarios:
        user_id = u["id"]
        nombre = u["nombre"]
        edad = u["edad"]
        canal = u["suscripcion"]
        streamer = u["streamer_favorito"]
        horarios = ", ".join(u["horario_recurrentes"])

        print(f"| {user_id:<4} | {nombre:<18} | {edad:<4} | {canal:<20} | {streamer:<20} | {horarios:<25} |")

    print("=" * ancho + "\n")

def imprimir_estadisticas():
    """Imprime el reporte completo cargando los datos internamente desde los JSON."""
    # Cargamos los datos aquí adentro
    usuarios = cargar_json("lista_usuarios.json")
    programas = cargar_json("lista_programas.json")

    # Si hubo un error al cargar y devolvieron listas vacías, cortamos la ejecución
    if not usuarios or not programas:
        print("Faltan datos para procesar el reporte.")
        return

    # Hacemos los análisis
    mejor_canal, conteo_canales = analizar_canales(usuarios)
    mejor_cat, conteo_cat = analizar_categorias(usuarios, programas)
    mejor_streamer, conteo_streamers = analizar_streamers(usuarios)
    mejor_horario, conteo_horarios = analizar_horarios(usuarios)
    streamer_pico = streamer_con_pico_de_vistas(usuarios, programas)

    
    print("\n" + "===" * 15)
    print(f"{'=== REPORTE DE ESTADÍSTICAS GLOBALES ===':^45}")
    print("===" * 15 + "\n")
    
    print(f"Total de usuarios registrados : {len(usuarios)}")
    print(f"Canal más visto (suscritos)   : {mejor_canal}")
    print(f"Categoría más vista           : {mejor_cat}")
    print(f"Streamer más visto            : {mejor_streamer}")
    print(f"Horario pico de visualización : {mejor_horario}")
    print(f"Streamer 'en racha' (en pico) : {streamer_pico}")

    # Función interna para imprimir los desgloses de manera ordenada
    def mostrar_desglose(titulo, diccionario, sufijo):
        print("\n" + "-" * 40)
        print(f"DETALLE: {titulo}")

        items_ordenados = sorted(diccionario.items(), key=lambda x: x[1], reverse=True)
        for clave, cantidad in items_ordenados:
            print(f"    • {clave:<20}: {cantidad} {sufijo}")

    mostrar_desglose("POR CATEGORÍA", conteo_cat, "vistas")
    mostrar_desglose("POR STREAMER", conteo_streamers, "vistas")
    mostrar_desglose("POR CANAL SUSCRITO", conteo_canales, "suscripciones")
    mostrar_desglose("POR HORARIO", conteo_horarios, "vistas")

    
    mostrar_tabla_usuarios(usuarios)



if __name__ == "__main__":

    imprimir_estadisticas()
