'''
En los lenguajes de programación, los comentarios suelen estar delimitados por símbolos específicos.
Vamos a modelar un reconocedor de comentarios para un lenguaje simplificado donde el alfabeto es 𝛴 =
{ /,*, a, b }.
1. Diseño: Construya el AFD que reconozca cadenas que comiencen con /*, terminen con */ y
contengan cualquier combinación de a y b en el medio.
2. Programación: Implemente en Python el autómata diseñado. El programa debe recibir una
cadena y devolver un valor booleano indicando si es un "Token de Comentario" válido.
'''

from collections import defaultdict


# Estados del autómata: A, B, C, D, E, F y G
AFN = {
    "alfabeto": {"/", "*", "a", "b"},
    "estado_inicial": "A",
    "estados_finales": {"G"},
    "transiciones": defaultdict(lambda: defaultdict(set)),
}


# Tabla de transiciones
AFN["transiciones"]["A"]["/"].add("B")
AFN["transiciones"]["B"]["*"].add("C")
AFN["transiciones"]["C"]["*"].add("F")
AFN["transiciones"]["C"]["a"].add("D")
AFN["transiciones"]["C"]["b"].add("E")
AFN["transiciones"]["D"]["*"].add("F")
AFN["transiciones"]["D"]["a"].add("D")
AFN["transiciones"]["D"]["b"].add("E")
AFN["transiciones"]["E"]["*"].add("F")
AFN["transiciones"]["E"]["a"].add("D")
AFN["transiciones"]["E"]["b"].add("E")
AFN["transiciones"]["F"]["/"].add("G")


def mover(estados, simbolo, transiciones):
    # Calcula a qué estados se puede ir leyendo un símbolo
    nuevos_estados = set()
    for estado in estados:
        nuevos_estados.update(transiciones[estado].get(simbolo, set()))
    return nuevos_estados


def es_comentario(cadena):
    # Rechaza si aparece un símbolo fuera del alfabeto
    if any(simbolo not in AFN["alfabeto"] for simbolo in cadena):
        return False

    # Empezamos en el estado inicial
    estados_actuales = {AFN["estado_inicial"]}

    # Leemos la cadena símbolo por símbolo
    for simbolo in cadena:
        estados_siguientes = mover(estados_actuales, simbolo, AFN["transiciones"])

        # Si no hay transición posible, se corta el recorrido
        if not estados_siguientes:
            return False

        estados_actuales = estados_siguientes

    # Acepta solo si se llega al estado final
    return any(estado in AFN["estados_finales"] for estado in estados_actuales)


if __name__ == "__main__":
    pruebas = [
        "/*/",
        "/**/",
        "/*aba*/",
        "/*a*/",
        "/*ab*/",
        "/*aab*/",
        "/*aaab*/",
        "/*aaab",
        "/*",
        "hola",
    ]

    for cadena in pruebas:
        print(f"{cadena}: {es_comentario(cadena)}")




