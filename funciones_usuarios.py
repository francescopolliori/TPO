from listas_usuarios import usuarios
from funciones_canales import validar_horario
from menu_seleccion import seleccionar_programa

def validarEdad(edad):
    if edad < 0:
        return -1
    else:
        return edad


def CargarUsuarios(matriz_usuario):
    usuario=[]
    nombre=input("Ingrese el nombre y apellido: ")
    edad=int(input("Ingrese la edad: "))
    edad=validarEdad(edad)
    while edad==-1:
        edad=int(input("Edad invalida, ingrese la edad nuevamente: "))
        edad=validarEdad(edad)
        
    prog=seleccionar_programa()
    streamer=input("Ingrese el streamer favorito: ")

    inicio_horario=input("Ingrese el inicio de su horario recurrente: ")
    while validar_horario(inicio_horario)==False:
        inicio_horario=input("Horario invalido, ingrese el inicio de su horario recurrente nuevamente: ")
    fin_horario=input("Ingrese el fin de su horario recurrente: ")
    while validar_horario(fin_horario)==False and inicio_horario>=fin_horario:
        fin_horario=input("Horario invalido, ingrese el fin de su horario recurrente nuevamente: ")

    usuario.append(len(matriz_usuario)+1)
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(prog)
    usuario.append(streamer)
    usuario.append([inicio_horario, fin_horario])
    matriz_usuario.append(usuario)
    return matriz_usuario
