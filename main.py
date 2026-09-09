from funciones_canales import menu_demostraciones
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
            menu_demostraciones()               
            
        # OPCIÓN 3 (una sola vez)
        elif opcion == '3':
            print("\n\033[H\033[2J") # Limpia la consola 
            imprimir_estadisticas(usuarios, programas, canales_validos)
            input("\nPresione ENTER para volver al menú principal...")
            
        # OPCIÓN 4: Salir
        elif opcion == '4':
            print("\nOperacion finalizada.")
            break
            
        else:
            print("\nOpción inválida. Por favor, intente nuevamente ingresando un número del 1 al 4.")

if __name__ == "__main__":
    menu_principal()