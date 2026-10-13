import re

from listas_usuarios import usuarios
from menu_seleccion import seleccionar_programa
from listas_programas import programas, canales_validos

PATRON_EDAD = r"[0-9]+"
PATRON_HORARIO = r"([01][0-9]|2[0-3]):([0-5][0-9])"


def validar_edad(edad):
    """Valida que la edad sea un entero entre 1 y 120. Devuelve -1 si no lo es."""
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
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos


def pedir_nombre():
    """Pide nombre y apellido hasta que tengan formato válido."""
    while True:
        nombre = input("Ingrese el nombre y apellido: ").strip()
        if validar_nombre(nombre):
            return nombre
        print("Nombre inválido. Use solo letras y separe nombre y apellido con un espacio.")


def pedir_edad():
    """Pide la edad hasta que sea un entero válido (1 a 120)."""
    while True:
        texto = input("Ingrese la edad: ").strip()
        if not re.fullmatch(PATRON_EDAD, texto):
            print("Debe ingresar un número entero.")
            continue
        edad = int(texto)
        if validar_edad(edad) != -1:
            return edad
        print("Edad inválida. Debe estar entre 1 y 120.")


def pedir_horario(mensaje, minimo=None):
    """Pide un horario HH:MM; si se indica 'minimo' (en minutos), debe ser posterior."""
    while True:
        horario = input(mensaje).strip()
        if validar_horario(horario):
            if minimo is None or horario_a_minutos(horario) > minimo:
                return horario
            print("El fin debe ser posterior al inicio.")
        else:
            print("Horario inválido. Use el formato HH:MM (ej: 09:30).")


def cargar_usuarios(matriz_usuario):
    """Función para cargar usuarios en la matriz de usuarios."""
    usuario = []
    nombre = pedir_nombre()
    edad = pedir_edad()

    prog = seleccionar_programa(edad)

    indice_streamer = programas.index(prog)

    nombre_canal = prog[2].lower()
    indice_canal = -1
    
    for i in range(len(canales_validos)):
        if canales_validos[i] == nombre_canal:
            indice_canal = i
            break

    inicio_horario = input("Ingrese el inicio de su horario recurrente(HH:MM): ")
    while not validar_horario(inicio_horario):
        inicio_horario = input("Horario invalido, ingrese el inicio de su horario recurrente nuevamente(HH:MM): ")

    fin_horario = input("Ingrese el fin de su horario recurrente(HH:MM): ")
    while True:
        if validar_horario(fin_horario) and horario_a_minutos(fin_horario) > horario_a_minutos(inicio_horario):
            break
        fin_horario = input("Horario invalido, ingrese el fin de su horario recurrente nuevamente (HH:MM): ")

    usuario.append(len(matriz_usuario) + 1)
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(indice_canal)
    usuario.append(indice_streamer)
    usuario.append([inicio_horario, fin_horario])

    matriz_usuario.append(usuario)
    return matriz_usuario


# Para probarlo
if __name__ == "__main__":
    cargar_usuarios(usuarios)
    print(usuarios)