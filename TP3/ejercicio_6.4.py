"""
Gramática 4 — Paréntesis Anidados
Producciones:
S → S(S)S
S → ε
Cadena de entrada:
(()())

Utilizando la gramática descrita anteriormente, desarrolle un script en Python que realice las siguientes tareas:
1. Pre-procesamiento (Filtrado): * El programa debe recibir una línea de código compleja
(ejemplo: if (x > (y + 1)) { print(x) }).
○ Debe filtrar y conservar únicamente los terminales del alfabeto 𝛴 = { ( , ) }.
○ Ejemplo de salida filtrada: (())()
2. Validación y Rastreo de Errores:
○ Si quiere reutilice la clase GramaticaGLC implementada en el Punto 6.2 para
verificar si la cadena filtrada pertenece al lenguaje generado por la gramática. O
puede implementar una nueva clase para analizarla.
○ Desafío: Si la cadena es rechazada, el programa debe identificar e informar el
índice del carácter donde se rompe la regla de formación (por ejemplo, un
paréntesis de cierre sin uno de apertura previo).
3. Visualización del "Linter":
○ El script debe imprimir la cadena original y, en la línea siguiente, utilizar un puntero
(ejemplo: ^) para señalar la posición exacta del error sintáctico detectado. 
"""

import re

class ValidadorParentesis:
    
    #Clase dedicada a validar paréntesis anidados.
    #Implementa el balanceo de paréntesis y detección de errores sintácticos.
    
    def __init__(self):
        # La gramática S -> S(S)S | ε define lenguajes de paréntesis balanceados.
        pass

    def es_valida(self, cadena):
        #Verifica si los paréntesis en la cadena están balanceados.
        pila = []
        for char in cadena:
            if char == '(':
                pila.append(char)
            elif char == ')':
                if not pila:
                    return False
                pila.pop()
        return len(pila) == 0

    def encontrar_posicion_error(self, cadena):
        #Retorna el índice del primer carácter que causa un error sintáctico. 
        #Si no hay errores, retorna None.
        pila = []
        for i, char in enumerate(cadena):
            if char == '(':
                pila.append(i)
            elif char == ')':
                if not pila:
                    # Error: paréntesis de cierre sin apertura
                    return i
                pila.pop()
        
        if pila:
            # Error: paréntesis de apertura sin cierre
            return pila[0]
            
        return None

def filtrar_cadena(cadena):
    #Filtra la cadena conservando solo los paréntesis '(' y ')'.
    return re.sub(r'[^()]', '', cadena)

def ejecutar_linter(cadena_original):
    #Procesa la cadena, valida los paréntesis y muestra el resultado del linter.
    
    print(f"\nCadena original: {cadena_original}")
    
    # 1. Pre-procesamiento
    cadena_filtrada = filtrar_cadena(cadena_original)
    
    validador = ValidadorParentesis()
    
    # 2. Validación
    if validador.es_valida(cadena_filtrada):
        print("Resultado: La cadena es sintácticamente correcta (paréntesis balanceados).")
    else:
        print("Resultado: La cadena tiene errores sintácticos.")
        
        # 3. Visualización del Linter y rastreo
        idx_error_filtrado = validador.encontrar_posicion_error(cadena_filtrada)
        
        if idx_error_filtrado is not None:
            # Mapear el índice del error de la cadena filtrada a la cadena original
            contador_filtrados = 0
            idx_original = -1
            
            for i, char in enumerate(cadena_original):
                if char in '()':
                    if contador_filtrados == idx_error_filtrado:
                        idx_original = i
                        break
                    contador_filtrados += 1
            
            if idx_original != -1:
                # Construir visualización del puntero
                puntero = " " * idx_original + "^"
                print(cadena_original)
                print(puntero)
                print(f"Error detectado en la posición {idx_original + 1}")
            else:
                print("Error detectado, pero no se pudo mapear a la posición en la cadena original.")

if __name__ == '__main__':
    # Casos de prueba
    ejemplos = [
        "(()())",
        "(( )) )",
        "(( )",
        "if (x > (y + 1)) { print(x) }",
        "if (x > (y + 1)) { print(x) )"
    ]
    
    for ej in ejemplos:
        ejecutar_linter(ej)
