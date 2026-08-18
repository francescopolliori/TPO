def CargarUsuarios(matriz_usuario):
    usuario=[]
    nombre=input("Ingrese el nombre y apellido: ")
    edad=int(input("Ingrese la edad: "))
    edad=validarEdad(edad)
    while edad==-1:
        edad=int(input("Edad invalida, ingrese la edad nuevamente: "))
        edad=validarEdad(edad)
        
    mail=input("Ingrese el correo electronico: ")
    prog=input("Ingrese el programa mas visto: ")

    
    usuario.append(nombre)
    usuario.append(edad)
    usuario.append(mail)
    usuario.append(prog)
    matriz_usuario.append(usuario)
