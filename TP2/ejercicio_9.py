'''
En los lenguajes de programación, los comentarios suelen estar delimitados por símbolos específicos.
Vamos a modelar un reconocedor de comentarios para un lenguaje simplificado donde el alfabeto es 𝛴 =
{ /,*, a, b }.
1. Diseño: Construya el AFD que reconozca cadenas que comiencen con /*, terminen con */ y
contengan cualquier combinación de a y b en el medio.
2. Programación: Implemente en Python el autómata diseñado. El programa debe recibir una
cadena y devolver un valor booleano indicando si es un "Token de Comentario" válido.
'''
import re

def es_comentario(cadena):
    # Expresión regular para reconocer el patrón /* ... */
    patron = r'^/\*([ab]*)\*/$'
    
    # Verificar si la cadena coincide con el patrón
    if re.match(patron, cadena):
        return True
    else:
        return False
    
# Pruebas de Unidad
pruebas = [
    "/*aba*/",
    "/*/",
    "/**/",
    "/*aaab",
]

for cadena in pruebas:
    print(f'{cadena}: {es_comentario(cadena)}')




