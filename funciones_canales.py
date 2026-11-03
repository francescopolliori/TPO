import json

RUTA_JSON = "programas.json"
DIAS_VALIDOS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

#FUNCIONES BASE Y ARCHIVOS
def limpiar_pantalla():
    """Limpia la consola usando códigos ANSI sin depender del sistema operativo (librería os)."""
    print("\033[H\033[2J", end="")

def cargar_json(ruta):
    """Carga los datos del JSON. Devuelve lista vacía si no existe."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def guardar_json(ruta, datos):
    """Guarda la lista de diccionarios en el archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def normalizar(texto):
    """Quita espacios, pasa a minúsculas y elimina tildes sin usar librerías."""
    texto = texto.strip().lower()
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for a, b in reemplazos:
        texto = texto.replace(a, b)
    return texto

#VALIDACIONES

def validar_horario(horario):
    horario = horario.strip()
    if len(horario) != 5 or horario[2] != ":":
        return False
    hh, mm = horario[:2], horario[3:]
    if not (hh.isdigit() and mm.isdigit()):
        return False
    return 0 <= int(hh) <= 23 and 0 <= int(mm) <= 59

def validar_dia(dia):
    return normalizar(dia) in DIAS_VALIDOS

#LÓGICA DE PROGRAMAS (CRUD)
def agregar_programa(ruta, nombre, streamer, canal, dia, horario, categoria):
    if not validar_dia(dia):
        raise ValueError("Día inválido.")
    if not validar_horario(horario):
        raise ValueError("Horario inválido. Use formato HH:MM.")

    programas = cargar_json(ruta)
    
    # Comprobamos si el canal es nuevo
    canales_existentes = {normalizar(p["plataforma"]) for p in programas}
    canal_nuevo = normalizar(canal) not in canales_existentes

    nuevo_programa = {
        "nombre_programa": nombre.strip(),
        "conductor": streamer.strip(),
        "plataforma": canal.strip(),
        "dia": dia.strip().capitalize(),
        "hora_inicio": horario.strip(),
        "genero": categoria.strip()
    }
    
    programas.append(nuevo_programa)
    guardar_json(ruta, programas)
    return canal_nuevo

def eliminar_programa(ruta, nombre_buscar):
    programas = cargar_json(ruta)
    nombre_buscado = normalizar(nombre_buscar)
    
    for p in programas:
        if normalizar(p["nombre_programa"]) == nombre_buscado:
            programas.remove(p)
            guardar_json(ruta, programas)
            return True
    return False

def actualizar_horario(ruta, nombre_buscar, nuevo_horario):
    if not validar_horario(nuevo_horario):
        raise ValueError("Horario inválido.")
        
    programas = cargar_json(ruta)
    nombre_buscado = normalizar(nombre_buscar)
    
    for p in programas:
        if normalizar(p["nombre_programa"]) == nombre_buscado:
            p["hora_inicio"] = nuevo_horario.strip()
            guardar_json(ruta, programas)
            return True
    return False

#REPORTES Y BÚSQUEDAS
def imprimir_programas(programas):
    """Imprime una tabla elegante."""
    if not programas:
        print("\n 📭 No hay programas para mostrar.\n")
        return

    ancho = 110
    print("\n" + "=" * ancho)
    print(f"| {'Programa':<25} | {'Conductor':<20} | {'Plataforma':<15} | {'Día':<10} | {'Hora':<6} | {'Género':<15} |")
    print("-" * ancho)

    for p in programas:
        nom = p["nombre_programa"][:24]
        cond = p["conductor"][:19]
        plat = p["plataforma"][:14]
        dia = p["dia"][:9]
        hora = p["hora_inicio"]
        gen = p["genero"][:14]
        print(f"| {nom:<25} | {cond:<20} | {plat:<15} | {dia:<10} | {hora:<6} | {gen:<15} |")
    
    print("=" * ancho + "\n")

def detectar_choques_horario(programas):
    choques = []
    for i in range(len(programas)):
        for j in range(i + 1, len(programas)):
            a, b = programas[i], programas[j]
            if normalizar(a["dia"]) == normalizar(b["dia"]) and a["hora_inicio"] == b["hora_inicio"]:
                choques.append((a["nombre_programa"], b["nombre_programa"], a["dia"], a["hora_inicio"]))
    return choques


# MENÚ INTERACTIVO
def menu_demostraciones():
    opciones = [
        "Agregar programa", 
        "Eliminar programa", 
        "Actualizar horario",
        "Listado completo", 
        "Buscar por canal", 
        "Buscar por streamer",
        "Nombres de todos los programas", 
        "Canales en mayúsculas",
        "Total de programas", 
        "Concatenación de nombres",
        "Choques de horario", 
        "Salir"
    ]

    seleccion = 0

    while True:
        programas = cargar_json(RUTA_JSON)
        limpiar_pantalla()
        
        print("===" * 15)
        print(f"{'MENÚ DE GESTIÓN DE PROGRAMAS':^55}")
        print("===" * 15 + "\n")

        for i, op in enumerate(opciones):
            marca = "➔ " if i == seleccion else "   "
            print(f"{marca} {i + 1:>2}. {op}")

        print("\n" + "=" * 55)
        accion = input(" Utilice (w/s) para moverse o el NÚMERO + ENTER: ").strip().lower()

        if accion == "w":
            seleccion = (seleccion - 1) % len(opciones)
            continue
        if accion == "s":
            seleccion = (seleccion + 1) % len(opciones)
            continue
        
        if accion.isdigit() and 1 <= int(accion) <= len(opciones):
            seleccion = int(accion) - 1
        elif accion != "":
            continue

        limpiar_pantalla()
        
        # --- EJECUCIÓN DE OPCIONES ---
        if seleccion == 0:
            print("=== AGREGAR PROGRAMA ===")
            nombre = input("Nombre del programa: ")
            streamer = input("Nombre del streamer: ")
            canal = input("Canal / Plataforma: ")
            dia = input("Día de transmisión: ")
            horario = input("Horario (HH:MM): ")
            categoria = input("Género: ")
            try:
                es_nuevo = agregar_programa(RUTA_JSON, nombre, streamer, canal, dia, horario, categoria)
                print("\nPrograma agregado con éxito.")
                if es_nuevo: print("Se registró una plataforma nueva.")
            except ValueError as e:
                print(f"\nError: {e}")

        elif seleccion == 1:
            print("=== ELIMINAR PROGRAMA ===")
            imprimir_programas(programas)
            nombre = input("Nombre del programa a eliminar: ")
            if eliminar_programa(RUTA_JSON, nombre):
                print("Programa eliminado.")
            else:
                print("No se encontró el programa.")

        elif seleccion == 2:
            print("=== ACTUALIZAR HORARIO ===")
            imprimir_programas(programas)
            nombre = input("Nombre del programa: ")
            nuevo = input("Nuevo horario (HH:MM): ")
            try:
                if actualizar_horario(RUTA_JSON, nombre, nuevo):
                    print("Horario actualizado.")
                else:
                    print("No se encontró el programa.")
            except ValueError as e:
                print(f"\nError: {e}")

        elif seleccion == 3:
            print("=== LISTADO COMPLETO ===")
            imprimir_programas(programas)

        elif seleccion == 4:
            print("=== BÚSQUEDA POR CANAL ===")
            canal_buscado = normalizar(input("Ingrese el nombre del canal: "))
            resultado = [p for p in programas if normalizar(p["plataforma"]) == canal_buscado]
            imprimir_programas(resultado)

        elif seleccion == 5:
            print("=== BÚSQUEDA POR STREAMER ===")
            streamer_buscado = normalizar(input("Ingrese el nombre del streamer: "))
            resultado = [p for p in programas if streamer_buscado in normalizar(p["conductor"])]
            imprimir_programas(resultado)

        elif seleccion == 6:
            print("=== NOMBRES DE TODOS LOS PROGRAMAS ===")
            nombres = [p["nombre_programa"] for p in programas]
            for n in nombres: print(f" - {n}")

        elif seleccion == 7:
            print("=== CANALES EN MAYÚSCULAS ===")
            canales = {p["plataforma"].upper() for p in programas}
            for c in canales: print(f" - {c}")

        elif seleccion == 8:
            print("=== TOTAL DE PROGRAMAS ===")
            print(f"Hay un total de {len(programas)} programas registrados.")

        elif seleccion == 9:
            print("=== CONCATENACIÓN DE NOMBRES ===")
            nombres = [p["nombre_programa"] for p in programas]
            print(" | ".join(nombres))

        elif seleccion == 10:
            print("=== CHOQUES DE HORARIO ===")
            choques = detectar_choques_horario(programas)
            if not choques:
                print("No hay choques de horario.")
            else:
                for a, b, dia, hora in choques:
                    print(f"Choque: '{a}' y '{b}' coinciden el {dia} a las {hora}.")

        elif seleccion == 11:
            print("Saliendo del menú... ¡Hasta luego!")
            break

        input("\nPresione ENTER para volver al menú...")

if __name__ == "__main__":
    menu_demostraciones()