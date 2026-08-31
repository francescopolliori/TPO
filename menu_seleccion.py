from listas_programas import programas

def seleccionar_programa(edad, solo_conductor=False):
    # 1. Filtramos por edad
    if edad >= 18:
        programas_filtrados = programas
    else:
        programas_filtrados = [p for p in programas if p[5] == "Infantil"]
        
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
        
        # 4. Filas dinámicas iterando sobre la lista filtrada
        for i, p in enumerate(programas_filtrados):
            prefijo = " ➔ " if i == seleccion else "   "
            
            if solo_conductor:
                print(f"{prefijo} {i:>3} | {p[1]:<20}")
            else:
                print(f"{prefijo} {i:>3} | {p[0]:<20} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10} | {p[4]:<5} | {p[5]:<15}")
                
        print("=" * ancho)
        
        accion = input("\n Acción (w/s) o ENTER: ").lower()
        
        if accion == 'w':
            seleccion = (seleccion - 1) % total
        elif accion == 's':
            seleccion = (seleccion + 1) % total
        elif accion == '':
            return programas_filtrados[seleccion]
    

if __name__ == "__main__":
    # Si se ejecuta directamente, mostramos el menú de selección
    print("Ejecutando menú de selección de programas...\n")
    # Ejecutamos la función y guardamos el índice devuelto
    posicion = seleccionar_programa(solo_conductor=True) # Cambiar a False si quieres ver todos los detalles

    # Limpiamos pantalla por última vez para mostrar el resultado
    print("\033[H\033[2J" + "\n" * 40)
    print(f"¡Programa seleccionado correctamente!")
    print(f"Posición devuelta (índice en la lista): {posicion}")
    print(f"Corresponde a: {programas[posicion][0]} (Plataforma: {programas[posicion][2]})")
