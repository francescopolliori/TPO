from unittest.mock import patch
import funciones_usuarios  

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

prueba_pedir_nombre()
prueba_pedir_edad()
prueba_horario_recurrente()