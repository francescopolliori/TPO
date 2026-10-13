from listas_usuarios import usuarios
from funciones_canales import validar_horario
from menu_seleccion import seleccionar_programa
from listas_programas import programas, canales_validos

def validar_edad(edad):
    """Valida que la edad sea un número entero positivo."""
    if edad < 0:
        return -1
    else:
        return edad


MINUTOS_DIA = 24 * 60

def horario_a_minutos(horario, referencia=None):
    """Convierte HH:MM a minutos. Si el horario es menor o igual
    que la referencia, lo interpreta como del día siguiente.
    """
    if not validar_horario(horario):
        raise ValueError(f"Horario '{horario}' inválido.")

    horas, minutos = map(int, horario.split(":"))
    total = horas * 60 + minutos

    if referencia is not None:
        if not validar_horario(referencia):
            raise ValueError(f"Horario de referencia '{referencia}' inválido.")

        horas_ref, minutos_ref = map(int, referencia.split(":"))
        minutos_referencia = horas_ref * 60 + minutos_ref

        if total <= minutos_referencia:
            total += MINUTOS_DIA

    return total


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

    indice_streamer = -1
    for i in range(len(programas)):
        if programas[i] == prog:
            indice_streamer = i
            break
        
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
    
        if validar_horario(fin_horario) and horario_a_minutos(fin_horario, inicio_horario) > horario_a_minutos(inicio_horario):
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