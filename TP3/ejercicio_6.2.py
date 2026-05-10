'''
Extienda la clase Gramatica (o cree una subclase GramaticaGLC) con los siguientes
métodos:
• derivar_izquierda(cadena): dado el símbolo inicial, realiza la derivación por
izquierda aplicando las producciones en orden hasta generar la cadena dada.
Muestra cada paso.
• derivar_derecha(cadena): ídem pero por derecha.
• pertenece(cadena): retorna True si la cadena puede ser generada por la gramática
(podés usar fuerza bruta para gramáticas pequeñas, o el algoritmo CYK si la
gramática está en FNC).
Ejemplo de uso esperado:
g = GramaticaGLC(
 terminales={'a', 'b'},
 no_terminales={'S'},
 simbolo_inicial='S',
 producciones={'S': ['aSb', 'ab']}
)
g.derivar_izquierda('aaabbb')
# Paso 1: S
# Paso 2: aSb
# Paso 3: aaSbb
# Paso 4: aaabbb
print(g.pertenece('aaabbb')) # → True
print(g.pertenece('aabb')) # → True
print(g.pertenece('aabbb')) # → False
'''

# importar la clase Gramatica del ejercicio anterior
from ejercicio_6_1 import Gramatica


class GramaticaGLC(Gramatica):
    # Constructor hereda del padre (Gramatica)
    def __init__(self, terminales, no_terminales, simbolo_inicial, producciones):
        super().__init__(terminales, no_terminales, simbolo_inicial, producciones)

    # Derivación por izquierda: reemplaza el no-terminal más a la izquierda
    def derivar_izquierda(self, cadena_objetivo):
        # iniciamos con el símbolo inicial
        actual = self.simbolo_inicial
        # contador de pasos para mostrar la progresión
        paso = 1

        # mostramos el primer paso (símbolo inicial)
        print(f"Paso {paso}: {actual}")

        # mientras no hayamos alcanzado la cadena objetivo
        while actual != cadena_objetivo:
            # buscamos el primer no-terminal (de izquierda a derecha)
            nt_encontrado = None
            for i in range(len(actual)):
                # si encontramos un no-terminal
                if actual[i] in self.no_terminales:
                    nt_encontrado = actual[i]
                    # guardar su posición
                    pos = i
                    # dejar de buscar (es el primero)
                    break

            # si no hay más no-terminales en la cadena
            if nt_encontrado is None:
                # la cadena solo tiene terminales, derivación fallida
                print("No se puede derivar más; la cadena no pertenece a la gramática.")
                # retorna False porque no alcanzamos el objetivo
                return False

            # obtener las alternativas de producción para ese no-terminal
            if nt_encontrado not in self.producciones:
                # el no-terminal no tiene producciones
                print("No hay producción disponible para", nt_encontrado)
                # retorna False porque no podemos derivar
                return False

            # probar cada alternativa de producción
            encontro_camino = False
            for alternativa in self.producciones[nt_encontrado]:
                # crear nueva cadena reemplazando el primer NT por esta alternativa
                nueva_cadena = actual[:pos] + alternativa + actual[pos+1:]

                # si la nueva cadena es igual al objetivo, usar esta alternativa
                if nueva_cadena == cadena_objetivo:
                    actual = nueva_cadena
                    paso = paso + 1
                    print(f"Paso {paso}: {actual}")
                    encontro_camino = True
                    # salir del bucle de alternativas
                    break

                # si la nueva cadena es más corta que el objetivo, no explorar
                if len(nueva_cadena) > len(cadena_objetivo):
                    continue

                # si la nueva cadena no contiene más no-terminales
                contiene_nt = any(ch in self.no_terminales for ch in nueva_cadena)
                if not contiene_nt and nueva_cadena != cadena_objetivo:
                    # no podemos seguir derivando
                    continue

                # usar esta alternativa si es promisoria
                actual = nueva_cadena
                paso = paso + 1
                print(f"Paso {paso}: {actual}")
                encontro_camino = True
                # salir del bucle de alternativas
                break

            # si ninguna alternativa funcionó
            if not encontro_camino:
                # no hay camino posible
                print("No se encontró derivación válida para esta cadena.")
                # retorna False porque no podemos derivar
                return False

            # evitar bucle infinito (máximo 100 pasos)
            if paso > 100:
                # si superamos 100 pasos, algo anda mal
                print("Máximo de pasos alcanzado; posible bucle infinito.")
                # retorna False porque no convergió
                return False

        # llegamos al objetivo, derivación exitosa
        print("Derivación exitosa!")
        # retorna True porque logramos generar la cadena objetivo
        return True

    # Derivación por derecha: reemplaza el no-terminal más a la derecha
    def derivar_derecha(self, cadena_objetivo):
        # iniciamos con el símbolo inicial
        actual = self.simbolo_inicial
        # contador de pasos para mostrar la progresión
        paso = 1

        # mostramos el primer paso (símbolo inicial)
        print(f"Paso {paso}: {actual}")

        # mientras no hayamos alcanzado la cadena objetivo
        while actual != cadena_objetivo:
            # buscamos el último no-terminal (de derecha a izquierda)
            nt_encontrado = None
            for i in range(len(actual) - 1, -1, -1):
                # si encontramos un no-terminal
                if actual[i] in self.no_terminales:
                    nt_encontrado = actual[i]
                    # guardar su posición
                    pos = i
                    # dejar de buscar (es el último)
                    break

            # si no hay más no-terminales en la cadena
            if nt_encontrado is None:
                # la cadena solo tiene terminales, derivación fallida
                print("No se puede derivar más; la cadena no pertenece a la gramática.")
                # retorna False porque no alcanzamos el objetivo
                return False

            # obtener las alternativas de producción para ese no-terminal
            if nt_encontrado not in self.producciones:
                # el no-terminal no tiene producciones
                print("No hay producción disponible para", nt_encontrado)
                # retorna False porque no podemos derivar
                return False

            # probar cada alternativa de producción
            encontro_camino = False
            for alternativa in self.producciones[nt_encontrado]:
                # crear nueva cadena reemplazando el último NT por esta alternativa
                nueva_cadena = actual[:pos] + alternativa + actual[pos+1:]

                # si la nueva cadena es igual al objetivo, usar esta alternativa
                if nueva_cadena == cadena_objetivo:
                    actual = nueva_cadena
                    paso = paso + 1
                    print(f"Paso {paso}: {actual}")
                    encontro_camino = True
                    # salir del bucle de alternativas
                    break

                # si la nueva cadena es más corta que el objetivo, no explorar
                if len(nueva_cadena) > len(cadena_objetivo):
                    continue

                # si la nueva cadena no contiene más no-terminales
                contiene_nt = any(ch in self.no_terminales for ch in nueva_cadena)
                if not contiene_nt and nueva_cadena != cadena_objetivo:
                    # no podemos seguir derivando
                    continue

                # usar esta alternativa si es promisoria
                actual = nueva_cadena
                paso = paso + 1
                print(f"Paso {paso}: {actual}")
                encontro_camino = True
                # salir del bucle de alternativas
                break

            # si ninguna alternativa funcionó
            if not encontro_camino:
                # no hay camino posible
                print("No se encontró derivación válida para esta cadena.")
                # retorna False porque no podemos derivar
                return False

            # evitar bucle infinito (máximo 100 pasos)
            if paso > 100:
                # si superamos 100 pasos, algo anda mal
                print("Máximo de pasos alcanzado; posible bucle infinito.")
                # retorna False porque no convergió
                return False

        # llegamos al objetivo, derivación exitosa
        print("Derivación exitosa!")
        # retorna True porque logramos generar la cadena objetivo
        return True

    # Verifica si una cadena pertenece al lenguaje generado por la gramática
    # usa fuerza bruta (búsqueda en amplitud) para explorar todas las derivaciones
    def pertenece(self, cadena):
        # cola de cadenas a explorar (iniciamos con el símbolo inicial)
        cola = [self.simbolo_inicial]
        # conjunto de cadenas ya visitadas para evitar repeticiones
        visitadas = set()

        # mientras hay cadenas en la cola
        while cola:
            # tomar la primera cadena de la cola
            actual = cola.pop(0)

            # si ya la visitamos, la ignoramos
            if actual in visitadas:
                continue

            # marcar como visitada
            visitadas.add(actual)

            # si la cadena actual es igual a la buscada
            if actual == cadena:
                # retorna True porque la cadena pertenece al lenguaje
                return True

            # si la cadena es más larga que la objetivo, descartarla
            if len(actual) > len(cadena):
                # saltear porque nunca podrá contraerse a la cadena
                continue

            # explorar todas las derivaciones posibles
            for i in range(len(actual)):
                # si encontramos un no-terminal
                if actual[i] in self.no_terminales:
                    # obtener sus alternativas de producción
                    if actual[i] in self.producciones:
                        # para cada alternativa de este no-terminal
                        for alternativa in self.producciones[actual[i]]:
                            # crear nueva cadena reemplazando el no-terminal
                            nueva_cadena = actual[:i] + alternativa + actual[i+1:]
                            # agregar a la cola si no la visitamos
                            if nueva_cadena not in visitadas:
                                cola.append(nueva_cadena)

        # si salimos del bucle sin encontrar la cadena
        print(f"La cadena '{cadena}' no pertenece al lenguaje.")
        # retorna False porque exhaustamos todas las posibilidades y no la hallamos
        return False

if __name__ == '__main__':
    # Crear una gramática para a^n b^n (n >= 1)
    g = GramaticaGLC(
        terminales={'a', 'b'},
        no_terminales={'S'},
        simbolo_inicial='S',
        producciones={'S': ['aSb', 'ab']}
    )

    print("Derivación por Izquierda")
    # derivar 'aaabbb' por izquierda
    g.derivar_izquierda('aaabbb')

    print("\nDerivación por Derecha")
    # derivar 'aabb' por derecha
    g.derivar_derecha('aabb')

    print("\nPruebas de Pertenencia")
    # testear si 'aaabbb' pertenece a la gramática
    print(f"¿'aaabbb' pertenece? {g.pertenece('aaabbb')}")
    # testear si 'aabb' pertenece a la gramática
    print(f"¿'aabb' pertenece? {g.pertenece('aabb')}")
    # testear si 'aabbb' pertenece a la gramática
    print(f"¿'aabbb' pertenece? {g.pertenece('aabbb')}")

