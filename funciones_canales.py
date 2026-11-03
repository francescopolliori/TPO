import json
import os
import sys
import unicodedata
from functools import reduce

# Las rutas son relativas a la carpeta del script, no al directorio de ejecución.
CARPETA = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(CARPETA, "lista_programas.json")

NOMBRE, STREAMER, CANAL, DIA, HORARIO, CATEGORIA = range(6)

dias_validos = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")

# Signos de puntuación permitidos además de letras, números y espacios.
PUNTUACION_PERMITIDA = set("_-.:,;'&!?()+#@")

# Ancho de cada columna de la tabla.
ANCHOS = (22, 22, 15, 14, 10)


def _soporta(texto):
    """Indica si la salida estándar puede mostrar el texto sin fallar."""
    codificacion = sys.stdout.encoding or "ascii"
    try:
        texto.encode(codificacion)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


# Símbolos con alternativa para consolas con codificación antigua.
FLECHA = "➔" if _soporta("➔") else ">"
PUNTOS = "…" if _soporta("…") else "..."


def _normalizar(texto):
    """Quita espacios sobrantes (extremos e internos) y pasa a minúsculas."""
    return " ".join(texto.split()).lower()


def _sin_acentos(texto):
    """Quita los acentos de un texto (á -> a). Solo se conserva la tilde de
    la ñ/Ñ; cualquier otra tilde (ã, õ...) se elimina."""
    resultado = []
    for c in unicodedata.normalize("NFD", texto):
        if unicodedata.category(c) == "Mn":
            if c == "\u0303" and resultado and resultado[-1] in "nN":
                resultado.append(c)
            continue
        resultado.append(c)
    return unicodedata.normalize("NFC", "".join(resultado))


def _clave_dia(dia):
    """Clave comparable para un día: sin espacios, sin tilde, en minúsculas."""
    return _sin_acentos(_normalizar(dia))


def _canales_de(programas):
    """Set con los canales (normalizados) que existen en los programas."""
    return {_normalizar(p[CANAL]) for p in programas}


def _recortar(texto, ancho):
    """Recorta un texto largo para que no desalinee la tabla."""
    if len(texto) < ancho:
        return texto
    return texto[:ancho - 1 - len(PUNTOS)] + PUNTOS


def _escribir_json_atomico(ruta, datos):
    """Escribe un JSON de forma atómica: primero a un archivo temporal y
    después lo reemplaza, así un corte a mitad de la escritura no destruye
    los datos existentes."""
    temporal = ruta + ".tmp"
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    except BaseException:
        try:
            os.remove(temporal)
        except OSError:
            pass
        raise


def _leer_json(ruta):
    """Devuelve la matriz de programas guardada en el JSON.
    Si el archivo no existe o está vacío devuelve una matriz vacía.
    Lanza ValueError si el JSON está dañado o tiene un formato inválido.
    Si el archivo trae una clave 'canales' (versiones anteriores) se ignora."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        return []

    if not texto.strip():
        return []

    try:
        contenido = json.loads(texto)
    except json.JSONDecodeError:
        raise ValueError(f"el archivo '{ruta}' está dañado.") from None

    programas = contenido.get("programas") if isinstance(contenido, dict) else contenido
    if not isinstance(programas, list):
        raise ValueError(f"el archivo '{ruta}' tiene un formato inválido.")
    for fila in programas:
        if (not isinstance(fila, list) or len(fila) != 6
                or not all(isinstance(campo, str) for campo in fila)):
            raise ValueError(f"el archivo '{ruta}' tiene un programa con formato inválido.")
    return programas


def _guardar_json(ruta, programas):
    """Guarda la matriz de programas en el JSON (escritura atómica)."""
    _escribir_json_atomico(ruta, {"programas": programas})


def guardar_resultado(nombre_archivo, resultados):
    """Guarda un resultado en un JSON (junto al script). Devuelve False si no
    pudo escribir, para que un error de disco no tire abajo el menú."""
    ruta = os.path.join(CARPETA, nombre_archivo)
    try:
        _escribir_json_atomico(ruta, resultados)
        return True
    except OSError:
        print(f"(Aviso: no se pudo guardar '{nombre_archivo}')")
        return False

#VALIDACIONES

def validar_horario(horario):
    """Valida que el horario tenga formato HH:MM en 24hs."""
    horario = horario.strip()
    if len(horario) != 5 or horario[2] != ":":
        return False
    hh, mm = horario[:2], horario[3:]
    # Solo dígitos ASCII: isdigit() acepta caracteres como '²' que rompen int().
    if not all(c in "0123456789" for c in hh + mm):
        return False
    return 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59


def validar_dia(dia):
    """Valida que el día sea válido, sin importar mayúsculas, tildes o espacios."""
    return _clave_dia(dia) in {_clave_dia(d) for d in dias_validos}


def validar_texto(texto):
    """Valida que un texto no esté vacío y contenga solo letras, números,
    espacios y algunos signos de puntuación comunes (_ - . : , ; ' & ! ? ( ) + # @)."""
    texto = texto.strip()
    if not texto:
        return False
    # Letras Unicode (con tildes y ñ) y solo dígitos ASCII: isalnum() acepta '²' o '½'.
    return all(c.isalpha() or c in "0123456789" or c == " " or c in PUNTUACION_PERMITIDA for c in texto)


def agregar_programa(ruta, nombre, streamer, canal, dia, horario, categoria):
    """Valida y agrega un programa al JSON.
    Devuelve True si el canal es nuevo.
    Lanza ValueError si algún dato es inválido o el programa ya existe."""
    for etiqueta, valor in (("nombre", nombre), ("streamer", streamer),
                            ("canal", canal), ("categoría", categoria)):
        if not validar_texto(valor):
            raise ValueError(f"{etiqueta} '{valor}' inválido.")
    if not validar_dia(dia):
        raise ValueError(f"día '{dia}' inválido.")
    if not validar_horario(horario):
        raise ValueError(f"horario '{horario}' inválido. Debe ser HH:MM.")

    dia_oficial = next(d for d in dias_validos if _clave_dia(d) == _clave_dia(dia))

    programas = _leer_json(ruta)
    nombre_buscado = _normalizar(nombre)
    if any(_normalizar(p[NOMBRE]) == nombre_buscado for p in programas):
        raise ValueError(f"ya existe un programa llamado '{' '.join(nombre.split())}'.")

    canal_limpio = " ".join(canal.split())
    canal_nuevo = _normalizar(canal_limpio) not in _canales_de(programas)

    programas.append([" ".join(nombre.split()), " ".join(streamer.split()), canal_limpio,dia_oficial, horario.strip(), " ".join(categoria.split())])
    _guardar_json(ruta, programas)
    return canal_nuevo


def eliminar_programa(ruta, nombre_programa):
    """Elimina un programa del JSON por nombre. Devuelve True si lo encontró."""
    programas = _leer_json(ruta)
    buscado = _normalizar(nombre_programa)
    for i, p in enumerate(programas):
        if _normalizar(p[NOMBRE]) == buscado:
            del programas[i]
            _guardar_json(ruta, programas)
            return True
    return False


def actualizar_horario(ruta, nombre_programa, nuevo_horario):
    """Cambia el horario de un programa en el JSON.
    Lanza ValueError con mensajes distintos si el horario es inválido o si el
    programa no existe."""
    if not validar_horario(nuevo_horario):
        raise ValueError(f"horario '{nuevo_horario}' inválido. Debe ser HH:MM.")
    programas = _leer_json(ruta)
    buscado = _normalizar(nombre_programa)
    for p in programas:
        if _normalizar(p[NOMBRE]) == buscado:
            p[HORARIO] = nuevo_horario.strip()
            _guardar_json(ruta, programas)
            return
    raise ValueError(f"no existe un programa llamado '{nombre_programa.strip()}'.")


# IMPRESIÓN / LISTADO
def imprimir_programas(programas):
    """Imprime la matriz con formato de tabla."""
    a = ANCHOS
    print(f"{'Programa':<{a[0]}}{'Streamer':<{a[1]}}{'Canal':<{a[2]}}"
          f"{'Día':<{a[3]}}{'Horario':<{a[4]}}Categoría")
    print("-" * (sum(a) + len("Categoría")))
    if not programas:
        print("No hay programas cargados.")
    for p in programas:
        print(f"{_recortar(p[NOMBRE], a[0]):<{a[0]}}"
              f"{_recortar(p[STREAMER], a[1]):<{a[1]}}"
              f"{_recortar(p[CANAL], a[2]):<{a[2]}}"
              f"{_recortar(p[DIA], a[3]):<{a[3]}}"
              f"{_recortar(p[HORARIO], a[4]):<{a[4]}}"
              f"{p[CATEGORIA]}")


def listado_completo(ruta):
    """Lee el JSON e imprime todos los programas en formato tabla."""
    imprimir_programas(_leer_json(ruta))


def buscar_por_canal(programas, canal):
    """Programas cuyo canal coincide exactamente (sin importar mayúsculas/espacios)."""
    canal = _normalizar(canal)
    if not canal:
        return []
    return list(filter(lambda p: _normalizar(p[CANAL]) == canal, programas))


def buscar_por_streamer(programas, streamer):
    """Programas cuyo streamer contiene el texto buscado. Un texto vacío no
    devuelve nada (en vez de devolver todos los programas)."""
    streamer = _normalizar(streamer)
    if not streamer:
        return []
    return list(filter(lambda p: streamer in _normalizar(p[STREAMER]), programas))


def obtener_nombres(programas):
    return list(map(lambda p: p[NOMBRE], programas))


def canales_en_mayusculas(programas):
    return list(map(lambda p: p[CANAL].upper(), programas))


def total_programas(programas):
    return reduce(lambda acc, p: acc + 1, programas, 0)


def concatenar_nombres(programas):
    return reduce(lambda acc, p: p[NOMBRE] if not acc else acc + " | " + p[NOMBRE],
                  programas, "")


def detectar_choques_horario(programas):
    """Pares de programas que coinciden en día y horario exactos."""
    choques = []
    for i in range(len(programas)):
        for j in range(i + 1, len(programas)):
            a, b = programas[i], programas[j]
            if _clave_dia(a[DIA]) == _clave_dia(b[DIA]) and a[HORARIO].strip() == b[HORARIO].strip():
                choques.append((a[NOMBRE], b[NOMBRE], a[DIA], a[HORARIO]))
    return choques


def choques_de_programa(programas, nombre_programa):
    """Choques de horario en los que participa un programa concreto."""
    buscado = _normalizar(nombre_programa)
    return [c for c in detectar_choques_horario(programas)
            if buscado in (_normalizar(c[0]), _normalizar(c[1]))]


def avisar_choques(ruta, nombre_programa):
    """Imprime una advertencia si el programa choca con otro."""
    try:
        choques = choques_de_programa(_leer_json(ruta), nombre_programa)
    except (ValueError, OSError):
        return
    for nombre_a, nombre_b, dia, horario in choques:
        print(f"\n(Aviso: '{nombre_a}' y '{nombre_b}' coinciden el {dia} a las {horario})")

# MENÚ DE DEMOSTRACIÓN DE FUNCIONES
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def menu_demostraciones():
    opciones = [
        "Agregar programa", "Eliminar programa", "Actualizar horario",
        "Listado completo", "Buscar por canal", "Buscar por streamer",
        "Nombres de todos los programas (map)", "Canales en mayúsculas (map)",
        "Total de programas (reduce)", "Concatenación de nombres (reduce)",
        "Choques de horario", "Salir"
    ]

    seleccion = 0

    while True:
        try:
            programas = _leer_json(ruta_json)
        except (ValueError, OSError) as error:
            print("Error:", error)
            input("\nPresione ENTER para salir...")
            break

        limpiar_pantalla()
        print("=" * 55)
        print("                 MENÚ DE FUNCIONES")
        print("=" * 55)

        for i in range(len(opciones)):
            marca = FLECHA if i == seleccion else " "
            print(f" {marca} {i + 1:>2}. {opciones[i]}")

        print("=" * 55)
        accion = input("\nw/s para moverse, número para elegir, ENTER para ejecutar: ").strip().lower()

        if accion == "w":
            seleccion = (seleccion - 1) % len(opciones)
            continue
        if accion == "s":
            seleccion = (seleccion + 1) % len(opciones)
            continue
        if accion != "":
            # Número de opción directo (solo dígitos ASCII).
            if all(c in "0123456789" for c in accion) and 1 <= int(accion) <= len(opciones):
                seleccion = int(accion) - 1
            else:
                continue

        limpiar_pantalla()

        if seleccion == 0:
            print("=== AGREGAR PROGRAMA ===")
            nombre = input("Ingrese el nombre del programa: ")
            streamer = input("Ingrese el nombre del streamer: ")
            canal = input("Ingrese el canal: ")
            dia = input("Ingrese el día: ")
            horario = input("Ingrese el horario (HH:MM): ")
            categoria = input("Ingrese la categoría: ")

            try:
                canal_nuevo = agregar_programa(ruta_json, nombre, streamer, canal,
                                               dia, horario, categoria)
                print("\nPrograma agregado correctamente.")
                if canal_nuevo:
                    print("Se creó un canal nuevo.")
                imprimir_programas(_leer_json(ruta_json))
                avisar_choques(ruta_json, nombre)
            except ValueError as error:
                print("\nNo se pudo agregar el programa:", error)
            except OSError:
                print("\nNo se pudo escribir el archivo.")

        elif seleccion == 1:
            print("=== ELIMINAR PROGRAMA ===")
            imprimir_programas(programas)
            nombre_programa = input("\nIngrese el nombre del programa que desea eliminar: ")
            try:
                if eliminar_programa(ruta_json, nombre_programa):
                    print("\nPrograma eliminado correctamente.")
                    imprimir_programas(_leer_json(ruta_json))
                else:
                    print("\nNo se encontró el programa.")
            except ValueError as error:
                print("\nNo se pudo eliminar el programa:", error)
            except OSError:
                print("\nNo se pudo escribir el archivo.")

        elif seleccion == 2:
            print("=== ACTUALIZAR HORARIO ===")
            imprimir_programas(programas)
            nombre_programa = input("\nIngrese el nombre del programa: ")
            nuevo_horario = input("Ingrese el nuevo horario (HH:MM): ")
            try:
                actualizar_horario(ruta_json, nombre_programa, nuevo_horario)
                print("\nHorario actualizado correctamente.")
                imprimir_programas(_leer_json(ruta_json))
                avisar_choques(ruta_json, nombre_programa)
            except ValueError as error:
                print("\nNo se pudo actualizar el horario:", error)
            except OSError:
                print("\nNo se pudo escribir el archivo.")

        elif seleccion == 3:
            print("=== LISTADO COMPLETO ===")
            imprimir_programas(programas)

        elif seleccion == 4:
            print("=== BÚSQUEDA POR CANAL ===")
            print("Canales disponibles:")
            for canal in sorted(_canales_de(programas)):
                print("- " + canal.upper())
            canal_buscado = input("\nIngrese el nombre del canal: ")
            resultado = buscar_por_canal(programas, canal_buscado)
            guardar_resultado("busqueda_canal.json", resultado)
            if not resultado:
                print("\nNo se encontraron programas del canal:", canal_buscado)
            else:
                print("\nProgramas encontrados:")
                imprimir_programas(resultado)

        elif seleccion == 5:
            print("=== BÚSQUEDA POR STREAMER ===")
            streamer_buscado = input("Ingrese el nombre del streamer: ")
            resultado = buscar_por_streamer(programas, streamer_buscado)
            guardar_resultado("busqueda_streamer.json", resultado)
            if not resultado:
                print("\nNo se encontraron streamers con el nombre:", streamer_buscado)
            else:
                print("\nProgramas encontrados:")
                imprimir_programas(resultado)

        elif seleccion == 6:
            print("=== NOMBRES DE TODOS LOS PROGRAMAS (MAP) ===")
            resultado = obtener_nombres(programas)
            guardar_resultado("nombres_programas.json", resultado)
            print(resultado)

        elif seleccion == 7:
            print("=== CANALES EN MAYÚSCULAS (MAP) ===")
            resultado = canales_en_mayusculas(programas)
            guardar_resultado("canales_mayusculas.json", resultado)
            print(resultado)

        elif seleccion == 8:
            print("=== TOTAL DE PROGRAMAS (REDUCE) ===")
            print(total_programas(programas))

        elif seleccion == 9:
            print("=== CONCATENACIÓN DE NOMBRES (REDUCE) ===")
            print(concatenar_nombres(programas))

        elif seleccion == 10:
            print("=== CHOQUES DE HORARIO ===")
            choques = detectar_choques_horario(programas)
            if not choques:
                print("No se encontraron choques de horario.")
            else:
                for nombre_a, nombre_b, dia, horario in choques:
                    print(f"- {nombre_a} y {nombre_b}: {dia} a las {horario}")

        elif seleccion == 11:
            print("Saliendo del menú...")
            break

        input("\nPresione ENTER para volver al menú...")


if __name__ == "__main__":
    try:
        menu_demostraciones()
    except (KeyboardInterrupt, EOFError):
        print("\nSaliendo del menú...")
        