from unittest.mock import patch
import funciones_usuarios
import generar_csv

#4 PRUEBAS UNITARIAS VALIDAS
#1. Se prueba pedir_nombre ingresando "Juan Perez", esperando como resultado "Juan Perez".
def prueba_pedir_nombre():
    with patch("builtins.input", return_value="Juan Perez"):
        nombre = funciones_usuarios.pedir_nombre()

    if nombre == "Juan Perez":
        print("Prueba de pedir_nombre: PASÓ")
    else:
        print("Prueba de pedir_nombre: FALLÓ")

#2. Se prueba pedir_edad ingresando 25, esperando como resultado 25.
def prueba_pedir_edad():
    with patch("builtins.input", return_value="25"):
        edad = funciones_usuarios.pedir_edad()

    if edad == 25:
        print("Prueba de pedir_edad: PASÓ")
    else:
        print("Prueba de pedir_edad: FALLÓ")

#3. Se prueba pedir_horario_recurrente ingresando "09:00" y "17:00", esperando como resultado ("09:00", "17:00").
def prueba_horario_recurrente():
    with patch("builtins.input", side_effect=["09:00", "17:00"]):
        inicio, fin = funciones_usuarios.pedir_horario_recurrente()

    if inicio == "09:00" and fin == "17:00":
        print("Prueba de pedir_horario_recurrente: PASÓ")
    else:
        print("Prueba de pedir_horario_recurrente: FALLÓ")

#4. Se prueba menu_exportacion ingresando "1", "2", "3" y "4" para generar los archivos CSV correspondientes.
def prueba_menu_exportacion():
    with patch("builtins.input", side_effect=["1", "2", "3", "4"]):
        generar_csv.menu_exportacion()

    print("Prueba de menu_exportacion: Si los archivos CSV se generaron correctamente, PASÓ. De lo contrario, FALLÓ.")

#3 PRUEBAS UNITARIAS INVALIDAS
#Primero se ingresa un valor invalido el cual se evita, luego uno válido para que la función pueda continuar y terminar correctamente.
#1. Se prueba pedir_nombre ingresando "" esperando como resultado un error
#Luego se ingresa "Juan Perez" para poder terminar la funcion correctamente.
def prueba_pedir_nombre_invalido():
    with patch("builtins.input", side_effect=["", "Juan Perez"]):
        nombre = funciones_usuarios.pedir_nombre()

    if nombre == "Juan Perez":
        print("Prueba de pedir_nombre (rechazo de inválido): PASÓ")
    else:
        print("Prueba de pedir_nombre (rechazo de inválido): FALLÓ")

#2. Se prueba pedir_edad ingresando "-5" esperando como resultado un error
#Luego se ingresa "25" para poder terminar la funcion correctamente.
def prueba_pedir_edad_invalida():
    with patch("builtins.input", side_effect=["-5", "25"]):
        edad = funciones_usuarios.pedir_edad()

    if edad == 25:
        print("Prueba de pedir_edad (inválido): PASÓ")
    else:
        print("Prueba de pedir_edad (inválido): FALLÓ")

#3. Se prueba pedir_horario_recurrente ingresando "25:00" esperando como resultado un error
#Luego se ingresa "09:00" y "17:00" para poder terminar la funcion correctamente.
def prueba_horario_recurrente_invalido():
    with patch("builtins.input", side_effect=["25:00","09:00", "17:00"]):
        inicio, fin = funciones_usuarios.pedir_horario_recurrente()

    if inicio == "09:00" and fin == "17:00":
        print("Prueba de pedir_horario_recurrente (inválido): PASÓ")
    else:
        print("Prueba de pedir_horario_recurrente (inválido): FALLÓ")

#PRUEBAS UNITARIAS CASOS EXTREMOS
#1. Se prueba validar_edad ingresando 120, esperando como resultado 120.
#Luego se ingresa 121, esperando como resultado -1.
def prueba_edad_limite():
    if funciones_usuarios.validar_edad(120) == 120 and \
funciones_usuarios.validar_edad(121) == -1:
        print("Prueba de edad límite: PASÓ")
    else:
        print("Prueba de edad límite: FALLÓ")

#2. Se prueba pedir_horario_recurrente ingresando "23:59" y "00:00", esperando como resultado ("23:59", "00:00").
def prueba_horario_cruza_medianoche():
    with patch("builtins.input", side_effect=["23:59", "00:00"]):
        inicio, fin = funciones_usuarios.pedir_horario_recurrente()

    if inicio == "23:59" and fin == "00:00":
        print("Prueba de horario al cruzar medianoche: PASÓ")
    else:
        print("Prueba de horario al cruzar medianoche: FALLÓ")

#PRUEBA UNITARIA ADICIONAL
#1. Se prueba cargar_usuarios ingresando dos usuarios iguales, esperando que tengan IDs diferentes
def prueba_usuarios_iguales_ids_diferentes():
    entradas = [
        "Juan Perez", "25", "", "09:00", "17:00",
        "Juan Perez", "25", "", "09:00", "17:00"
    ]

    with patch("builtins.input", side_effect=entradas):
        usuarios1 = funciones_usuarios.cargar_usuarios()
        usuarios2 = funciones_usuarios.cargar_usuarios()

    if usuarios2[-2]["id"] != usuarios2[-1]["id"]:
        print("Prueba de usuarios iguales con IDs diferentes: PASÓ")
    else:
        print("Prueba de usuarios iguales con IDs diferentes: FALLÓ")

prueba_pedir_nombre()
prueba_pedir_edad()
prueba_horario_recurrente()
prueba_menu_exportacion()
prueba_pedir_nombre_invalido()
prueba_pedir_edad_invalida()
prueba_horario_recurrente_invalido()
prueba_edad_limite()
prueba_horario_cruza_medianoche()
prueba_usuarios_iguales_ids_diferentes()