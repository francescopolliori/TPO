from listas_programas import programas

def seleccionar_programa():
    seleccion = 0
    total = len(programas)
    
    while True:
        # Limpiamos la pantalla con saltos de línea y código ANSI 
        # (funciona sin importar la librería os)
        print("\033[H\033[2J" + "\n" * 40)
        
        print("=" * 105)
        print(" MENÚ DE SELECCIÓN DE PROGRAMAS ".center(105, "="))
        print(" Usa 'w' (subir) o 's' (bajar) + ENTER. Presioná solo ENTER para elegir ".center(105, " "))
        print("=" * 105)
        
        print(f"    {'Nº':>3} | {'Programa':<20} | {'Conductor':<20} | {'Plataforma':<10} | {'Día':<10} | {'Hora':<5}")
        print("-" * 105)
        
        for i, p in enumerate(programas):
            if i == seleccion:
                # Fila seleccionada: mostramos la flecha
                print(f" ➔  {i:>3} | {p[0]:<20} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10} | {p[4]:<5}")
            else:
                print(f"    {i:>3} | {p[0]:<20} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10} | {p[4]:<5}")
                
        print("=" * 105)
        
        # Capturamos la acción del usuario
        accion = input("\n Acción (w/s) o ENTER: ").lower()
        
        if accion == 'w':
            seleccion = (seleccion - 1) % total  # Sube
        elif accion == 's':
            seleccion = (seleccion + 1) % total  # Baja
        elif accion == '':
            return seleccion # Si presiona ENTER vacío, devuelve la posición


if __name__ == "__main__":
    # Si se ejecuta directamente, mostramos el menú de selección
    print("Ejecutando menú de selección de programas...\n")
    # Ejecutamos la función y guardamos el índice devuelto
    posicion = seleccionar_programa()

    # Limpiamos pantalla por última vez para mostrar el resultado
    print("\033[H\033[2J" + "\n" * 40)
    print(f"¡Programa seleccionado correctamente!")
    print(f"Posición devuelta (índice en la lista): {posicion}")
    print(f"Corresponde a: {programas[posicion][0]} (Plataforma: {programas[posicion][2]})")
