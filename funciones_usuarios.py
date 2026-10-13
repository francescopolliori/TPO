import re

from listas_usuarios import usuarios
from funciones_canales import validar_horario
from menu_seleccion import seleccionar_programa
from listas_programas import programas

def validarEdad(edad):
    """Valida que la edad sea un número entero positivo."""
    if edad < 0:
        return -1
    else:
        return edad


def horario_a_minutos(horario):
    """Convierte un horario en formato HH:MM a minutos totales."""
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos

def ingresar_nombre():
    """Función para ingresar el nombre del usuario."""
    while True:
        nombre = input("Ingrese el nombre y apellido: ")
        if nombre.strip() == "":
            print("El nombre no puede estar vacío. Intente nuevamente.")
        elif not re.match("^[a-zA-Z ]+$", nombre):
            print("El nombre solo puede contener letras y espacios. Intente nuevamente.")
        elif not re.match("^[A-Z][a-z]+ [A-Z][a-z]+$", nombre):
            print("El nombre debe tener el formato 'Nombre Apellido'. Intente nuevamente.")
        else:
            break
    return nombre

def cargarUsuarios(matriz_usuario):
    """Función para cargar usuarios en la matriz de usuarios."""
    usuario=[]
    nombre = ingresar_nombre()
    edad=int(input("Ingrese la edad: "))
    edad=validarEdad(edad)
    while edad==-1:
        edad=int(input("Edad invalida, ingrese la edad nuevamente: "))
        edad=validarEdad(edad)
        
    prog=seleccionar_programa()
    streamer=programas[prog][1]

    inicio_horario=input("Ingrese el inicio de su horario recurrente(HH:MM): ")
    while validar_horario(inicio_horario)==False:
        inicio_horario=input("Horario invalido, ingrese el inicio de su horario recurrente nuevamente(HH:MM): ")

    fin_horario=input("Ingrese el fin de su horario recurrente(HH:MM): ")
    while True:
        if validar_horario(fin_horario) and horario_a_minutos(fin_horario) > horario_a_minutos(inicio_horario):
            break
        fin_horario=input("Horario invalido, ingrese el fin de su horario recurrente nuevamente (debe ser posterior al inicio)(HH:MM): ")

    usuario.append(len(matriz_usuario)+1)
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(prog)
    usuario.append(streamer)
    usuario.append([inicio_horario, fin_horario])
    matriz_usuario.append(usuario)
    return matriz_usuario

#Para probarlo creen una lista vacia y llamen a la funcion cargarUsuarios(lista_vacia) e imprimanla

cargarUsuarios(usuarios)