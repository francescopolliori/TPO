from funciones_canales import agregar_programa, actualizar_horario
from funciones_usuarios import cargar_usuarios
from administrador import imprimir_estadisticas
from listas_usuarios import usuarios
from listas_programas import programas, canales_validos

def menu_principal():
    """Menú interactivo principal que integra todas las funcionalidades."""
    while True:
        print("\n" + "=" * 55)
        print("                 MENÚ PRINCIPAL")
        print("=" * 55)
        print("  1. Ingresar usuarios")
        print("  2. Cargar/modificar programas")
        print("  3. Analizar estadísticas")
        print("  4. Finalizar")
        print("=" * 55)
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        # OPCIÓN 1
        if opcion == '1':
            print("\n--- Ingreso de Usuarios ---")
            while True:
                cargar_usuarios(usuarios)
                print("\n¡Usuario cargado exitosamente!")
                
                continuar = input("¿Desea ingresar otro usuario? (s/n): ").strip().lower()
                if continuar != 's':
                    print("Regresando al menú principal...")
                    break 
        
        # OPCIÓN 2
        elif opcion == '2':
            print("\n--- Cargar / Modificar Programas ---")
            while True:
                print("\n  A. Agregar un nuevo programa")
                print("  B. Modificar el horario de un programa existente")
                sub_op = input("Seleccione una opción (A/B): ").strip().upper()
                
                if sub_op == 'A':
                    print("\n-- Nuevo Programa --")
                    nombre = input("Nombre del programa: ")
                    streamer = input("Conductor/Streamer: ")
                    canal = input("Canal: ")
                    dia = input("Día de transmisión: ")
                    horario = input("Horario (HH:MM): ")
                    categoria = input("Categoría: ")
                    
                    # La función internamente validará y agregará a la lista
                    agregar_programa(programas, nombre, streamer, canal, dia, horario, categoria)
                    print("Intento de carga finalizado (revisa si el sistema arrojó algún error de validación).")
                    
                elif sub_op == 'B':
                    print("\n-- Modificar Horario --")
                    nombre = input("Ingrese el nombre exacto del programa a modificar: ")
                    nuevo_horario = input("Ingrese el nuevo horario (HH:MM): ")
                    
                    exito = actualizar_horario(programas, nombre, nuevo_horario)
                    if exito:
                        print("¡Horario actualizado exitosamente!")
                    else:
                        print("Error: No se pudo actualizar (revisa que el nombre exista y el formato del horario sea correcto).")
                else:
                    print("Opción inválida.")
                
                continuar = input("\n¿Desea cargar/modificar otro programa? (s/n): ").strip().lower()
                if continuar != 's':
                    print("Regresando al menú principal...")
                    break
            
        # OPCIÓN 3 (una sola vez)
        elif opcion == '3':
            print("\n\033[H\033[2J") # Limpia la consola 
            imprimir_estadisticas(usuarios, programas, canales_validos)
            input("\nPresione ENTER para volver al menú principal...")
            
        # OPCIÓN 4: Salir
        elif opcion == '4':
            print("\nSaliendo del programa... ¡Hasta luego!")
            break
            
        else:
            print("\nOpción inválida. Por favor, intente nuevamente ingresando un número del 1 al 4.")

if __name__ == "__main__":
    menu_principal()