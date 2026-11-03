import re
import json

from menu_seleccion import cargar_programas, seleccionar_programa



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
        if not palabra.replace("-", "").replace("'", "").isalpha():
            return False
    return True


def validar_horario(horario):
    """Valida el formato HH:MM (00:00 a 23:59), con dos dígitos en cada parte."""
    return re.match(r"^([01][0-9]|2[0-3]):([0-5][0-9])$", horario) is not None


def horario_a_minutos(horario, referencia=None):
    """Convierte HH:MM a minutos. Si el horario es menor o igual
    que la referencia, lo interpreta como del día siguiente.
    """
    MINUTOS_DIA = 24 * 60

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
        if not re.match(r"^[0-9]+$", texto):
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


def pedir_horario_recurrente():
    """Pide y valida el inicio y el fin de un horario recurrente."""
    inicio_horario = input("Ingrese el inicio de su horario recurrente(HH:MM): ").strip()
    while not validar_horario(inicio_horario):
        inicio_horario = input("Horario invalido, ingrese el inicio de su horario recurrente nuevamente(HH:MM): ").strip()

    fin_horario = input("Ingrese el fin de su horario recurrente(HH:MM): ").strip()
    while True:
        if (validar_horario(fin_horario) and horario_a_minutos(fin_horario, inicio_horario) > horario_a_minutos(inicio_horario)):
            return inicio_horario, fin_horario
        fin_horario = input(
            "Horario invalido, ingrese el fin de su horario recurrente nuevamente (HH:MM): ").strip()



def cargar_usuarios(usuarios):
    """Carga un usuario y lo guarda en lista_usuarios.json."""
    programas = cargar_programas()
    if not programas:
        print("No hay programas disponibles para registrar el usuario.")
        return usuarios

    nombre = pedir_nombre()
    edad = pedir_edad()

    prog = seleccionar_programa(programas, edad)
    if prog is None:
        return usuarios

    inicio_horario, fin_horario = pedir_horario_recurrente()

    usuario = {
        "id": max((u.get("id", 0) for u in usuarios), default=0) + 1,
        "nombre": nombre, 
        "edad": edad, 
        "suscripcion": prog["nombre_programa"],
        "streamer_favorito": prog["conductor"],
        "horario_recurrentes": [inicio_horario, fin_horario]
    }

    usuarios.append(usuario)
    with open("lista_usuarios.json", "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)
    return usuarios


# Para probarlo
if __name__ == "__main__":
    with open("lista_usuarios.json", "r", encoding="utf-8") as archivo:
        usuarios = json.load(archivo)
    cargar_usuarios(usuarios)
    print(usuarios)