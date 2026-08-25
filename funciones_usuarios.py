from listas_usuarios import usuarios
from funciones_canales import validar_horario
from menu_seleccion import seleccionar_programa

def validarEdad(edad):
    if edad < 0:
        return -1
    else:
        return edad


def horario_a_minutos(horario):
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos


def cargarUsuarios(matriz_usuario):
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
    while True:
        if validar_horario(fin_horario) and horario_a_minutos(fin_horario) > horario_a_minutos(inicio_horario):
            break
        fin_horario=input("Horario invalido, ingrese el fin de su horario recurrente nuevamente (debe ser posterior al inicio): ")

    usuario.append(len(matriz_usuario)+1)
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(prog)
    usuario.append(streamer)
    usuario.append([inicio_horario, fin_horario])
    matriz_usuario.append(usuario)
    return matriz_usuario
