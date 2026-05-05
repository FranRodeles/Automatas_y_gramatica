# Expresión regular: (b|a)*abb


transiciones = {
    'A': {'a': 'B', 'b': 'C'},
    'B': {'a': 'B', 'b': 'D'},
    'C': {'a': 'B', 'b': 'C'},
    'D': {'a': 'B', 'b': 'E'},
    'E': {'a': 'B', 'b': 'C'}
}

estado_inicial = 'A'
estado_final = 'E'


def acepta(cadena):
    estado = estado_inicial

    for letra in cadena:
        estado = transiciones[estado][letra]

    return estado == estado_final


# Pruebas
cadenas = ["abb", "aabb", "ab", "babb", "bbba"]

for c in cadenas:
    if acepta(c):
        print(c, "-> Aceptada")
    else:
        print(c, "-> Rechazada")


