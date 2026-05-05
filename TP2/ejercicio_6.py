#Expresión regular: (a | b)*(a | b | ε)
#EJERCICIO N° 6
#a) Utilizando la construcción de subconjuntos, pasar el AFN del ejercicio N° 4 a un AFD (mostrar tabla completa).
#b) Programar en Python el AFD resultante

# AFD convertido desde AFN

estado_actual = "A"

print("Estados: A, B, C")
print("Estado inicial: A")
print("Estado final: C")
print("Alfabeto permitido: a, b")

cadena = input("Ingrese una cadena: ")

valido = True

for simbolo in cadena:
    if simbolo == "a":
        if estado_actual == "A":
            estado_actual = "B"
        elif estado_actual == "B":
            estado_actual = "B"
        elif estado_actual == "C":
            estado_actual = "B"

    elif simbolo == "b":
        if estado_actual == "A":
            estado_actual = "C"
        elif estado_actual == "B":
            estado_actual = "C"
        elif estado_actual == "C":
            estado_actual = "C"

    else:
        valido = False
        break

if not valido:
    print("Cadena inválida (solo se permiten a y b)")
else:
    if estado_actual == "C":
        print("Cadena ACEPTADA")
    else:
        print("Cadena RECHAZADA")