import json
from functools import reduce
import re

ruta_json="lista_programas.json"



NOMBRE, STREAMER, CANAL, DIA, HORARIO, CATEGORIA = range(6)

dias_validos = ( "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")

#Json lectura de archivos
RE_HORARIO = re.compile(r"([01]\d|2[0-3]):[0-5]\d")
RE_TEXTO = re.compile(r"[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+")


def _canales_de(programas):
    """Set con los canales (normalizados) que existen en los programas."""
    return {" ".join(p[CANAL].split()).lower() for p in programas}


def _leer_json(ruta):
    """Devuelve la matriz de programas guardada en el JSON.
    Si el archivo no existe devuelve una matriz vacía.
    Lanza ValueError si el JSON está dañado o tiene un formato inválido."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            programas = json.load(archivo)["programas"]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError):
        raise ValueError(f"el archivo '{ruta}' está dañado o tiene un formato inválido.")
    for fila in programas:
        if not isinstance(fila, list) or len(fila) != 6:
            raise ValueError(f"el archivo '{ruta}' tiene un programa con formato inválido.")
    return programas


def _guardar_json(ruta, programas):
    """Guarda la matriz y el set de canales (como lista) en el JSON.
    Lanza OSError si no se puede escribir el archivo."""
    datos = {"programas": programas, "canales": sorted(_canales_de(programas))}
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


#VALIDACIONES
def validar_horario(horario):
    """Valida que el horario tenga formato HH:MM en 24hs."""
    if len(horario) != 5 or horario[2] != ":":
        return False
    hh, mm = horario[0:2], horario[3:5]
    for c in hh + mm:
        if not ('0' <= c <= '9'):
            return False
    return 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59


def validar_dia(dia):
    """Valida que el día sea uno de los días válidos de la semana."""
    return dia.lower() in dias_validos


def validar_texto(texto):
    """Valida que un texto no esté vacío y contenga solo letras, números
    y espacios, sin usar regex."""
    texto = texto.strip()
    if not texto:
        return False
    for caracter in texto:
        es_letra_minuscula = ("a" <= caracter <= "z") or caracter in "aáéíóúñ"
        es_letra_mayuscula = ("A" <= caracter <= "Z") or caracter in "AÁÉÍÓÚÑ"
        es_numero = "0" <= caracter <= "9"
        es_espacio = caracter == " "
        if not (es_letra_minuscula or es_letra_mayuscula or es_numero or es_espacio):
            return False
    return True


# AGREGAR PROGRAMA
def agregar_programa(ruta, nombre, streamer, canal, dia, horario, categoria):
    """Valida y agrega un programa al JSON. Cualquier canal es válido: si ya
    existe no se vuelve a agregar a la lista de canales (set).
    Lanza ValueError si un dato es inválido, OSError si falla el archivo.
    Devuelve True si el canal era nuevo, False si ya existía."""
    for etiqueta, valor in (("nombre", nombre), ("streamer", streamer),
                            ("canal", canal), ("categoría", categoria)):
        if not RE_TEXTO.fullmatch(valor.strip()):
            raise ValueError(f"{etiqueta} '{valor}' inválido.")

    dia_oficial = next((d for d in dias_validos if d.lower() == dia.strip().lower()), None)
    if dia_oficial is None:
        raise ValueError(f"día '{dia}' inválido.")
    if not RE_HORARIO.fullmatch(horario.strip()):
        raise ValueError(f"horario '{horario}' inválido. Debe ser HH:MM.")

    programas = _leer_json(ruta)
    canal_limpio = " ".join(canal.split())
    canal_nuevo = canal_limpio.lower() not in _canales_de(programas)

    programas.append([nombre.strip(), streamer.strip(), canal_limpio,
                      dia_oficial, horario.strip(), categoria.strip()])
    _guardar_json(ruta, programas)
    return canal_nuevo


# ELIMINAR PROGRAMA
def eliminar_programa(ruta, nombre_programa):
    """Elimina un programa del JSON por nombre (ignora mayúsculas).
    Devuelve True si lo eliminó, False si no existe."""
    programas = _leer_json(ruta)
    for p in programas:
        if p[NOMBRE].lower() == nombre_programa.strip().lower():
            programas.remove(p)
            _guardar_json(ruta, programas)
            return True
    return False


# ACTUALIZAR HORARIO
def actualizar_horario(ruta, nombre_programa, nuevo_horario):
    """Cambia el horario de un programa en el JSON.
    Devuelve False si el horario es inválido o el programa no existe."""
    if not RE_HORARIO.fullmatch(nuevo_horario.strip()):
        return False
    programas = _leer_json(ruta)
    for p in programas:
        if p[NOMBRE].lower() == nombre_programa.strip().lower():
            p[HORARIO] = nuevo_horario.strip()
            _guardar_json(ruta, programas)
            return True
    return False


# LISTADO COMPLETO
def listado_completo(ruta):
    """Lee el JSON e imprime todos los programas en formato tabla."""
    programas = _leer_json(ruta)
    print(f"{'Programa':<22}{'Streamer':<22}{'Canal':<15}{'Dia':<14}{'Horario':<10}Categoria")
    print("-" * 100)
    if not programas:
        print("No hay programas cargados.")
    for p in programas:
        print(f"{p[NOMBRE]:<22}{p[STREAMER]:<22}{p[CANAL]:<15}"
              f"{p[DIA]:<14}{p[HORARIO]:<10}{p[CATEGORIA]}")


#IMPRESIÓN
def imprimir_programas(programas):
    """Imprime la matriz con formato de tabla."""
    print(
        f"{'Programa':<22}"
        f"{'Streamer':<22}"
        f"{'Canal':<15}"
        f"{'Dia':<14}"
        f"{'Horario':<10}"
        f"{'Categoria'}"
    )
    print("-" * 100)
    for p in programas:
        print(
            f"{p[NOMBRE]:<22}"
            f"{p[STREAMER]:<22}"
            f"{p[CANAL]:<15}"
            f"{p[DIA]:<14}"
            f"{p[HORARIO]:<10}"
            f"{p[CATEGORIA]}"
        )


#BÚSQUEDAS 
def buscar_por_canal(programas, canal, nombre_archivo="lista_programa.json"):
    """Búsqueda exacta: encuentra todos los programas de un canal específico."""
    resultados =list(filter(lambda p: p[CANAL].lower() == canal.lower(), programas))
    """Guarda los resultados en un archivo JSON."""
    with open(nombre_archivo,"w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii=False)
   
    return resultados

def buscar_por_streamer(programas, streamer,nombre_archivo="busqueda_streamer.json"):
    """Búsqueda parcial: encuentra el streamer aunque escriban solo una parte del nombre."""
    resultados = list(filter(lambda p: streamer.lower() in p[STREAMER].lower(), programas))
    """"Guarda los resultados en un archivo JSON."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(resultados,archivo, indent=4, ensure_ascii=False)

    return resultados

#TRANSFORMACIONES
def obtener_nombres(programas,nombre_archivo="nombres_programas.json"):
    """Devuelve una lista solo con los nombres de los programas."""
    resultados= list(map(lambda p: p[NOMBRE], programas))
    """Guarda los resultados en un archivo JSON."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii=False)

    return resultados   

def canales_en_mayusculas(programas,nombre_archivo="canales_mayusculas.json"):
    """Devuelve la lista de canales, todos en mayúsculas."""
    resultados = list(map(lambda p: p[CANAL].upper(), programas))
    """Guarda los resultados en un archivo JSON."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii=False)

    return resultados

#ACUMULACIONES
def total_programas():
    """Cuenta el total de programas del JSON usando reduce."""
    with open("lista_programas.json", "r", encoding="utf-8") as archivo:
        programas = json.load(archivo)

    return reduce(lambda acc, p: acc + 1, programas, 0)


def concatenar_nombres():
    """Concatena los nombres de los programas del JSON usando reduce."""
    with open("lista_programas.json", "r", encoding="utf-8") as archivo:
        programas = json.load(archivo)

    return reduce(
        lambda acc, p: acc + p["nombre_programa"] + " | ",
        programas,
        ""
    )


#ESTADÍSTICAS
def detectar_choques_horario():
    """Devuelve pares de programas que van el mismo día y horario."""

    with open("lista_programas.json", "r", encoding="utf-8") as archivo:
        programas = json.load(archivo)

    choques = []

    for i in range(len(programas)):
        for j in range(i + 1, len(programas)):
            if (programas[i]["dia"] == programas[j]["dia"]
                    and programas[i]["hora_inicio"] == programas[j]["hora_inicio"]):

                choques.append((
                    programas[i]["nombre_programa"],
                    programas[j]["nombre_programa"],
                    programas[i]["dia"],
                    programas[i]["hora_inicio"]
                ))

    return choques

def abrir_json(ruta):
    """Abre un archivo JSON y devuelve su contenido como un diccionario."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# MENÚ DE DEMOSTRACIÓN DE FUNCIONES
def menu_demostraciones():

    opciones = [
        "Agregar programa",
        "Eliminar programa",
        "Actualizar horario",
        "Listado completo",
        "Buscar por canal",
        "Buscar por streamer",
        "Nombres de todos los programas (map)",
        "Canales en mayúsculas (map)",
        "Total de programas (reduce)",
        "Concatenación de nombres (reduce)",
        "Choques de horario",
        "Salir"
    ]

    seleccion = 0

    while True:
        print("\033[H\033[2J" + "\n" * 20)

        print("=" * 55)
        print("          MENÚ DE FUNCIONES")
        print("=" * 55)

        for i in range(len(opciones)):
            if i == seleccion:
                print(" ➔ " + opciones[i])
            else:
                print("   " + opciones[i])

        print("=" * 55)

        accion = input("\nAcción (w/s) o ENTER: ").lower()

        if accion == "w":
            seleccion = (seleccion - 1) % len(opciones)

        elif accion == "s":
            seleccion = (seleccion + 1) % len(opciones)

        elif accion == "":
            print("\033[H\033[2J" + "\n" * 10)

            # AGREGAR PROGRAMA
            if seleccion == 0:
                print("=== AGREGAR PROGRAMA ===")

                nombre = input("Ingrese el nombre del programa: ")
                streamer = input("Ingrese el nombre del streamer: ")
                canal = input("Ingrese el canal: ")
                dia = input("Ingrese el día: ")
                horario = input("Ingrese el horario (HH:MM): ")
                categoria = input("Ingrese la categoría: ")

                cantidad_anterior = len(abrir_json("lista_programas.json"))
                programas=abrir_json("lista_programas.json")["programas"]

                agregar_programa(
                    programas,
                    nombre,
                    streamer,
                    canal,
                    dia,
                    horario,
                    categoria
                )

                if len(programas) > cantidad_anterior:
                    print("\nPrograma agregado correctamente.")
                    imprimir_programas(programas)
                else:
                    print("\nNo se pudo agregar el programa.")

            # ELIMINAR PROGRAMA
            elif seleccion == 1:
                print("=== ELIMINAR PROGRAMA ===")

                imprimir_programas(programas)

                nombre_programa = input(
                    "\nIngrese el nombre del programa que desea eliminar: "
                )

                eliminado = eliminar_programa(
                    programas,
                    nombre_programa
                )

                if eliminado:
                    print("\nPrograma eliminado correctamente.")
                    imprimir_programas(programas)
                else:
                    print("\nNo se encontró el programa.")

            # ACTUALIZAR HORARIO
            elif seleccion == 2:
                print("=== ACTUALIZAR HORARIO ===")

                imprimir_programas(programas)

                nombre_programa = input(
                    "\nIngrese el nombre del programa: "
                )

                nuevo_horario = input(
                    "Ingrese el nuevo horario (HH:MM): "
                )

                actualizado = actualizar_horario(
                    programas,
                    nombre_programa,
                    nuevo_horario
                )

                if actualizado:
                    print("\nHorario actualizado correctamente.")
                    imprimir_programas(programas)
                else:
                    print(
                        "\nNo se pudo actualizar el horario. "
                        "Verifique el nombre y el horario ingresados."
                    )

            # LISTADO COMPLETO
            elif seleccion == 3:
                print("=== LISTADO COMPLETO ===")
                imprimir_programas(programas)


            # BÚSQUEDA POR CANAL
            elif seleccion == 4:
                print("=== BÚSQUEDA POR CANAL ===")

                print("Canales disponibles:")

                for canal in programas:
                    print("- " + canal.upper())

                canal_buscado = input(
                    "\nIngrese el nombre del canal: "
                )

                resultado = buscar_por_canal(
                    programas,
                    canal_buscado
                )

                if len(resultado) == 0:
                    print(
                        "\nNo se encontraron programas del canal:",
                        canal_buscado
                    )
                else:
                    print("\nProgramas encontrados:")
                    imprimir_programas(resultado)

            # BÚSQUEDA POR STREAMER
            elif seleccion == 5:
                print("=== BÚSQUEDA POR STREAMER ===")

                streamer_buscado = input(
                    "Ingrese el nombre o una parte "
                    "del nombre del streamer: "
                )

                resultado = buscar_por_streamer(
                    programas,
                    streamer_buscado
                )

                if len(resultado) == 0:
                    print(
                        "\nNo se encontraron streamers con el nombre:",
                        streamer_buscado
                    )
                else:
                    print("\nProgramas encontrados:")
                    imprimir_programas(resultado)

            # NOMBRES DE LOS PROGRAMAS
            elif seleccion == 6:
                print("=== NOMBRES DE TODOS LOS PROGRAMAS (MAP) ===")
                print(obtener_nombres(programas))

            # CANALES EN MAYÚSCULAS
            elif seleccion == 7:
                print("=== CANALES EN MAYÚSCULAS (MAP) ===")
                print(canales_en_mayusculas(programas))

            # TOTAL DE PROGRAMAS
            elif seleccion == 8:
                print("=== TOTAL DE PROGRAMAS (REDUCE) ===")
                print(total_programas())

            # CONCATENAR NOMBRES
            elif seleccion == 9:
                print("=== CONCATENACIÓN DE NOMBRES (REDUCE) ===")
                print(concatenar_nombres())

            # CHOQUES DE HORARIO
            elif seleccion == 10:
                print("=== CHOQUES DE HORARIO ===")

                choques = detectar_choques_horario()

                if len(choques) == 0:
                    print("No se encontraron choques de horario.")
                else:
                    print(choques)

            # SALIR
            elif seleccion == 11:
                print("Saliendo del menú...")
                break

            input("\nPresione ENTER para volver al menú...")


if __name__ == "__main__":
    menu_demostraciones()