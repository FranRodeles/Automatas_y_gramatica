'''
Dada la expresión regular: (a | b)*(a | b | ε)
a) Realizar el AFN mediante la construcción de Thompson.
b) Programar en Python el AFN obtenido.
'''
import re

def validar_cadena(cadena):
    # 
    patron = r'^[ab]*(a|b|)$'
    return re.match(patron, cadena) is not None

# Ejemplo de uso
cadenas = ["", "a", "b", "ab", "ba", "aabb", "abc", "aab", "bba", "c"]
for cadena in cadenas:
    print(f"{cadena}: {'Válida' if validar_cadena(cadena) else 'Inválida'}")

