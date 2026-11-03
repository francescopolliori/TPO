from unittest.mock import patch
import funciones_usuarios
import generar_csv

#4 PRUEBAS UNITARIAS VALIDAS
def prueba_pedir_nombre():
    with patch("builtins.input", return_value="Juan Perez"):
        nombre = funciones_usuarios.pedir_nombre()

    if nombre == "Juan Perez":
        print("Prueba de pedir_nombre: PASÓ")
    else:
        print("Prueba de pedir_nombre: FALLÓ")

def prueba_pedir_edad():
    with patch("builtins.input", return_value="25"):
        edad = funciones_usuarios.pedir_edad()

    if edad == 25:
        print("Prueba de pedir_edad: PASÓ")
    else:
        print("Prueba de pedir_edad: FALLÓ")

def prueba_horario_recurrente():
    with patch("builtins.input", side_effect=["09:00", "17:00"]):
        inicio, fin = funciones_usuarios.pedir_horario_recurrente()

    if inicio == "09:00" and fin == "17:00":
        print("Prueba de pedir_horario_recurrente: PASÓ")
    else:
        print("Prueba de pedir_horario_recurrente: FALLÓ")

def prueba_menu_exportacion():
    with patch("builtins.input", side_effect=["1", "2", "3", "4"]):
        generar_csv.menu_exportacion()

    print("Prueba de menu_exportacion: PASÓ (verifique los archivos CSV generados)")

#3 PRUEBAS UNITARIAS INVALIDAS
#Primero se ingresa un valor invalido el cual se evita, luego uno válido para que la función pueda continuar y terminar correctamente.
def prueba_pedir_nombre_invalido():
    with patch("builtins.input", side_effect=["", "Juan Perez"]):
        nombre = funciones_usuarios.pedir_nombre()

    if nombre == "Juan Perez":
        print("Prueba de pedir_nombre (rechazo de inválido): PASÓ")
    else:
        print("Prueba de pedir_nombre (rechazo de inválido): FALLÓ")

def prueba_pedir_edad_invalida():
    with patch("builtins.input", side_effect=["-5", "25"]):
        edad = funciones_usuarios.pedir_edad()

    if edad == 25:
        print("Prueba de pedir_edad (inválido): PASÓ")
    else:
        print("Prueba de pedir_edad (inválido): FALLÓ")

def prueba_horario_recurrente_invalido():
    with patch("builtins.input", side_effect=["25:00","09:00", "17:00"]):
        inicio, fin = funciones_usuarios.pedir_horario_recurrente()

    if inicio == "09:00" and fin == "17:00":
        print("Prueba de pedir_horario_recurrente (inválido): PASÓ")
    else:
        print("Prueba de pedir_horario_recurrente (inválido): FALLÓ")


prueba_pedir_nombre()
prueba_pedir_edad()
prueba_horario_recurrente()
prueba_menu_exportacion()
prueba_pedir_nombre_invalido()
prueba_pedir_edad_invalida()
prueba_horario_recurrente_invalido()