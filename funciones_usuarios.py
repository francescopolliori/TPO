import re

from listas_usuarios import usuarios
from menu_seleccion import seleccionar_programa
from listas_programas import programas, canales_validos

PATRON_EDAD = r"[0-9]+"
PATRON_HORARIO = r"([01][0-9]|2[0-3]):([0-5][0-9])"


def validar_edad(edad):
    """Valida que la edad sea un número entero positivo."""
    if edad <= 0 or edad > 120:
        return -1
    else:
        return edad


def validar_nombre(nombre):
    """Valida que el nombre tenga al menos dos palabras formadas solo por letras."""
    palabras = nombre.split()
    if len(palabras) < 2:
        return False
    for palabra in palabras:
        # se permiten guiones y apóstrofes dentro de una palabra (ej: Pérez-Gómez, O'Brien)
        if not palabra.replace("-", "").replace("'", "").isalpha():
            return False
    return True


def validar_horario(horario):
    """Valida el formato HH:MM (00:00 a 23:59), con dos dígitos en cada parte."""
    return re.fullmatch(PATRON_HORARIO, horario) is not None


def horario_a_minutos(horario):
    """Convierte un horario en formato HH:MM a minutos totales."""
    coincidencia = re.fullmatch(PATRON_HORARIO, horario)
    if coincidencia is None:
        raise ValueError(f"Horario inválido: {horario!r}")
    horas, minutos = map(int, coincidencia.groups())
    return horas * 60 + minutos


def cargar_usuarios(matriz_usuario):
    """Función para cargar usuarios en la matriz de usuarios."""
    usuario=[]
    nombre=input("Ingrese el nombre y apellido: ")
    edad=int(input("Ingrese la edad: "))
    edad=validar_edad(edad)
    while edad==-1:
        edad=int(input("Edad invalida, ingrese la edad nuevamente: "))
        edad=validar_edad(edad)
        

    prog = seleccionar_programa(edad)

    indice_streamer = programas.index(prog)

    nombre_canal = prog[2].lower()
    try:
        indice_canal = canales_validos.index(nombre_canal)
    except ValueError:
        print(f"Canal '{nombre_canal}' no encontrado en canales_validos.")
        return matriz_usuario  # cancela la carga en vez de guardar un -1

    inicio_horario = pedir_horario("Ingrese el inicio de su horario recurrente (HH:MM): ")
    fin_horario = pedir_horario(
        "Ingrese el fin de su horario recurrente (HH:MM): ",
        minimo=horario_a_minutos(inicio_horario),
    )

    usuario.append(len(matriz_usuario) + 1)
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(indice_canal)
    usuario.append(indice_streamer)
    usuario.append([inicio_horario, fin_horario])

    matriz_usuario.append(usuario)
    return matriz_usuario

#Para probarlo 
if __name__ == "__main__":
    cargar_usuarios(usuarios)
    print(usuarios)