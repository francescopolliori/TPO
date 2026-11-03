import json

def cargar_programas():
    """Carga y devuelve la lista de programas desde un archivo JSON."""
    try:
        with open("lista_programas.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo 'lista_programas.json'.")
        return []

def seleccionar_programa(programas, edad, solo_conductor=False):
    """Muestra un menú de selección de programas o de conductores según la 
    edad del usuario y devuelve el programa seleccionado (diccionario)."""
    
    # 1. Filtramos por edad usando la clave 'genero'
    if edad >= 18:
        programas_filtrados = programas
    else:
        programas_filtrados = [p for p in programas if p.get("genero") == "Infantil"]
        
    seleccion = 0
    total = len(programas_filtrados)
    
    if total == 0:
        print("No hay programas disponibles para tu edad.")
        return None
    
    while True:
        print("\033[H\033[2J" + "\n" * 40)

        # 2. Ajustamos el ancho según el modo de visualización
        ancho = 40 if solo_conductor else 125
        print("=" * ancho)
        
        # 3. Encabezados dinámicos
        if solo_conductor:
            print(f"    {'Nº':>3} | {'Conductor':<20}")
        else:
            print(f"    {'Nº':>3} | {'Programa':<20} | {'Conductor':<20} | {'Plataforma':<10} | {'Día':<10} | {'Hora':<5} | {'Género':<15}")
            
        print("-" * ancho)
        
        # 4. Filas dinámicas iterando sobre los diccionarios
        for i, p in enumerate(programas_filtrados):
            prefijo = " ➔ " if i == seleccion else "   "
            
            if solo_conductor:
                print(f"{prefijo} {i:>3} | {p['conductor']:<20}")
            else:
                print(f"{prefijo} {i:>3} | {p['nombre_programa']:<20} | {p['conductor']:<20} | {p['plataforma']:<10} | {p['dia']:<10} | {p['hora_inicio']:<5} | {p['genero']:<15}")
                
        print("=" * ancho)
        
        accion = input("\n Acción (w/s) o ENTER: ").lower()
        
        if accion == 'w':
            seleccion = (seleccion - 1) % total
        elif accion == 's':
            seleccion = (seleccion + 1) % total
        elif accion == '':
            return programas_filtrados[seleccion]


if __name__ == "__main__":
    # Cargamos los datos del archivo JSON
    programas = cargar_programas()

    if programas:
        print("Ejecutando menú de selección de programas...\n")
        
        # Ejecutamos la función pasando la lista cargada
        programa_seleccionado = seleccionar_programa(programas, edad=18, solo_conductor=False)

        # Limpiamos pantalla para mostrar el resultado
        print("\033[H\033[2J" + "\n" * 40)
        if programa_seleccionado:
            print("¡Programa seleccionado correctamente!")
            print(f"Nombre: {programa_seleccionado['nombre_programa']}")
            print(f"Conductor: {programa_seleccionado['conductor']}")
            print(f"Plataforma: {programa_seleccionado['plataforma']}")