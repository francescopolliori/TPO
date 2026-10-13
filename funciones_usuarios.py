from listas_usuarios import usuarios
from funciones_canales import validar_horario
from menu_seleccion import seleccionar_programa
from listas_programas import programas, canales_validos

def validar_edad(edad):
    """Valida que la edad sea un número entero positivo."""
    if edad <= 0:
        return -1
    else:
        return edad


def horario_a_minutos(horario):
    """Convierte un horario en formato HH:MM a minutos totales."""
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos

def pedir_edad():
    """Pide la edad hasta que sea un entero positivo."""
    while True:
        try:
            edad = int(input("Ingrese la edad: "))
        except ValueError:
            print("Debe ingresar un número entero.")
            continue
        if validar_edad(edad) != -1:
            return edad
        print("Edad inválida.")

def cargar_usuarios(matriz_usuario):
    """Función para cargar usuarios en la matriz de usuarios."""
    usuario=[]
    nombre=input("Ingrese el nombre y apellido: ")
    edad = pedir_edad()
        

    prog = seleccionar_programa(edad)

    indice_streamer = programas.index(prog)

    nombre_canal = prog[2].lower()
    try:
        indice_canal = canales_validos.index(nombre_canal)
    except ValueError:
        print(f"Canal '{nombre_canal}' no encontrado en canales_validos.")
        return matriz_usuario  # cancela la carga en vez de guardar un -1

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

#Para probarlo 
if __name__ == "__main__":
    cargar_usuarios(usuarios)
    print(usuarios)