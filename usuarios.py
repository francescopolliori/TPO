def validarEdad(edad):
    if edad < 0:
        return -1

    if edad < 16:
        return False
    else:
        return True