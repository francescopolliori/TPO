from functools import reduce
from listas_programas import programas, DIAS_VALIDOS, canales_validos

NOMBRE, STREAMER, CANAL, DIA, HORARIO, CATEGORIA = range(6)



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
    return dia.lower() in DIAS_VALIDOS


def validar_texto(texto):
    """Valida que un texto no esté vacío y contenga solo letras, números
    y espacios, sin usar regex."""
    texto = texto.strip()
    if not texto:
        return False
    for caracter in texto:
        es_letra_minuscula = "a" <= caracter <= "z"
        es_letra_mayuscula = "A" <= caracter <= "Z"
        es_numero = "0" <= caracter <= "9"
        es_espacio = caracter == " "
        if not (es_letra_minuscula or es_letra_mayuscula or es_numero or es_espacio):
            return False
    return True


def validar_canal(canal):
    """Valida que el canal esté dentro de la lista de canales conocidos."""
    return canal.lower() in canales_validos


# ALTA / BAJA / MODIFICACIÓN 
def agregar_programa(programas, nombre, streamer, canal, dia, horario, categoria):
    """Agrega un nuevo programa a la matriz, validando todos los campos."""
    if not validar_texto(nombre):
        print(f"Error: nombre '{nombre}' inválido.")
        return programas
    if not validar_texto(streamer):
        print(f"Error: streamer '{streamer}' inválido.")
        return programas
    if not validar_canal(canal):
        print(f"Error: canal '{canal}' inválido.")
        return programas
    if not validar_dia(dia):
        print(f"Error: día '{dia}' inválido.")
        return programas
    if not validar_horario(horario):
        print(f"Error: horario '{horario}' inválido. Debe ser formato HH:MM.")
        return programas
    if not validar_texto(categoria):
        print(f"Error: categoría '{categoria}' inválida.")
        return programas
    programas.append([nombre, streamer, canal, dia, horario, categoria])
    return programas


def actualizar_horario(programas, nombre_programa, nuevo_horario):
    """Modifica el horario de un programa existente, validando el formato."""
    if not validar_horario(nuevo_horario):
        print(f"Error: horario '{nuevo_horario}' inválido.")
        return False
    for p in programas:
        if p[NOMBRE].lower() == nombre_programa.lower():
            p[HORARIO] = nuevo_horario
            return True
    return False


def eliminar_programa(programas, nombre_programa):
    """Elimina un programa de la matriz por nombre."""
    for p in programas:
        if p[NOMBRE].lower() == nombre_programa.lower():
            programas.remove(p)
            return True
    return False


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
def buscar_por_canal(programas, canal):
    return list(filter(lambda p: p[CANAL].lower() == canal.lower(), programas))


def buscar_por_dia(programas, dia):
    return list(filter(lambda p: p[DIA].lower() == dia.lower(), programas))


def buscar_por_categoria(programas, categoria):
    return list(filter(lambda p: p[CATEGORIA].lower() == categoria.lower(), programas))


def buscar_por_streamer(programas, streamer):
    """Búsqueda parcial: encuentra el streamer aunque escriban solo una parte del nombre."""
    return list(filter(lambda p: streamer.lower() in p[STREAMER].lower(), programas))


def buscar_por_nombre(programas, nombre):
    """Búsqueda parcial por nombre de programa."""
    return list(filter(lambda p: nombre.lower() in p[NOMBRE].lower(), programas))


#TRANSFORMACIONES
def obtener_nombres(programas):
    """Devuelve una lista solo con los nombres de los programas."""
    return list(map(lambda p: p[NOMBRE], programas))


def canales_en_mayusculas(programas):
    """Devuelve la lista de canales, todos en mayúsculas."""
    return list(map(lambda p: p[CANAL].upper(), programas))


#ACUMULACIONES
def total_programas(programas):
    """Cuenta el total de programas usando reduce."""
    return reduce(lambda acc, p: acc + 1, programas, 0)


def concatenar_nombres(programas):
    """Concatena todos los nombres de programas en un solo string."""
    return reduce(lambda acc, p: acc + p[NOMBRE] + " | ", programas, "")


#ORDENAMIENTO
def ordenar_por_horario(programas):
    return sorted(programas, key=lambda p: p[HORARIO])


def ordenar_por_dia(programas):
    orden_dias = {
        "Lunes": 0, "Martes": 1, "Miercoles": 2, "Jueves": 3,
        "Viernes": 4, "Sabado": 5, "Domingo": 6,
    }
    return sorted(programas, key=lambda p: orden_dias.get(p[DIA], 99))


def ordenar_por_canal(programas):
    return sorted(programas, key=lambda p: p[CANAL])


#ESTADÍSTICAS
def contar_por_canal(programas):
    """Cuenta cuántos programas hay por canal."""
    conteo = {}
    for p in programas:
        conteo[p[CANAL]] = conteo.get(p[CANAL], 0) + 1
    return conteo


def canales_unicos(programas):
    return sorted(set(map(lambda p: p[CANAL], programas)))


def categorias_unicas(programas):
    return sorted(set(map(lambda p: p[CATEGORIA], programas)))


def detectar_choques_horario(programas):
    """Devuelve pares de programas que van el mismo día y horario."""
    choques = []
    for i in range(len(programas)):
        for j in range(i + 1, len(programas)):
            if (programas[i][DIA] == programas[j][DIA]
                    and programas[i][HORARIO] == programas[j][HORARIO]):
                choques.append((
                    programas[i][NOMBRE], programas[j][NOMBRE],
                    programas[i][DIA], programas[i][HORARIO]
                ))
    return choques


# MENÚ DE DEMOSTRACIÓN DE FUNCIONES
def menu_demostraciones():
    opciones = [
        "Agregar programa válido",
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
        # limpiar la consola
        print("\033[H\033[2J" + "\n" * 20)

        print("=" * 55)
        print("          DEMOSTRACIÓN DE FUNCIONES")
        print("=" * 55)

        # Muestra todas las opciones
        for i in range(len(opciones)):
            if i == seleccion:
                print(" ➔ " + opciones[i])
            else:
                print("   " + opciones[i])

        print("=" * 55)

        accion = input("\nAcción (w/s) o ENTER: ").lower()

        # Moverse hacia arriba
        if accion == "w":
            seleccion = (seleccion - 1) % len(opciones)

        # Moverse hacia abajo
        elif accion == "s":
            seleccion = (seleccion + 1) % len(opciones)

        # Ejecutar la opción seleccionada
        elif accion == "":
            print("\033[H\033[2J" + "\n" * 10)

            # AGREGAR UN PROGRAMA VÁLIDO
            if seleccion == 0:
                print("=== AGREGAR PROGRAMA VÁLIDO ===")

                # Copiamos la matriz para no modificar la lista original
                programas_prueba = []

                for programa in programas:
                    programas_prueba.append(programa.copy())

                agregar_programa(
                    programas_prueba,
                    "Nuevo Show",
                    "Un Streamer",
                    "TWITCH",
                    "Domingo",
                    "20:00",
                    "Humor"
                )

                imprimir_programas(programas_prueba)

            # MOSTRAR TODOS LOS PROGRAMAS
            elif seleccion == 1:
                print("=== LISTADO COMPLETO ===")
                imprimir_programas(programas)

            # BUSCAR PROGRAMAS POR CANAL
            elif seleccion == 2:
                print("=== BÚSQUEDA POR CANAL ===")

                print("Canales disponibles:")

                for canal in canales_validos:
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

            # BUSCAR PROGRAMAS POR STREAMER
            elif seleccion == 3:
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

            # CONSEGUIR LOS NOMBRES CON MAP
            elif seleccion == 4:
                print("=== NOMBRES DE TODOS LOS PROGRAMAS (MAP) ===")
                print(obtener_nombres(programas))

            # CONVERTIR LOS CANALES A MAYÚSCULAS CON MAP
            elif seleccion == 5:
                print("=== CANALES EN MAYÚSCULAS (MAP) ===")
                print(canales_en_mayusculas(programas))

            # CONTAR PROGRAMAS CON REDUCE
            elif seleccion == 6:
                print("=== TOTAL DE PROGRAMAS (REDUCE) ===")
                print(total_programas(programas))

            # CONCATENAR NOMBRES CON REDUCE
            elif seleccion == 7:
                print("=== CONCATENACIÓN DE NOMBRES (REDUCE) ===")
                print(concatenar_nombres(programas))

            # DETECTAR PROGRAMAS EN EL MISMO DÍA Y HORARIO
            elif seleccion == 8:
                print("=== CHOQUES DE HORARIO ===")

                choques = detectar_choques_horario(programas)

                if len(choques) == 0:
                    print("No se encontraron choques de horario.")
                else:
                    print(choques)

            # SALIR DEL MENÚ
            elif seleccion == 9:
                print("Saliendo del menú...")
                break

            input("\nPresione ENTER para volver al menú...")


# EJECUTAR MENÚ
if __name__ == "__main__":
    menu_demostraciones()