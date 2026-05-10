'''
Versión con nombre de módulo válido para importar la clase Gramatica de forma normal.
Se mantiene la misma lógica del ejercicio 6.1.
'''

class Gramatica:
    # Constructor: recibe conjuntos de terminales/no terminales,
    # símbolo inicial y un diccionario de producciones.
    def __init__(self, terminales, no_terminales, simbolo_inicial, producciones):
        # Guardar los parámetros en atributos de instancia
        self.terminales = set(terminales)
        self.no_terminales = set(no_terminales)
        self.simbolo_inicial = simbolo_inicial
        # producciones: mapeo 'A' -> ['aB', 'b', 'ε']
        self.producciones = {nt: list(rhs) for nt, rhs in producciones.items()}

    # Comprueba si la gramática es regular (Tipo 3).
    # Regla simple: todas las RHS tienen a lo sumo un no-terminal,
    # y si existe, está al inicio o al final.
    def es_regular(self):
        for A, rhss in self.producciones.items():
            # LHS debe ser un único no terminal
            if A not in self.no_terminales:
                return False

            for r in rhss:
                # 'ε' es válido en gramáticas regulares
                if r == 'ε' or r == '':
                    continue

                # posiciones de no terminales en RHS
                nt_positions = [i for i, ch in enumerate(r) if ch in self.no_terminales]

                # debe haber 0 o 1 no terminal
                if len(nt_positions) > 1:
                    return False

                # si hay 1 no terminal, debe estar al principio o al final
                if len(nt_positions) == 1:
                    pos = nt_positions[0]
                    if pos != 0 and pos != len(r) - 1:
                        return False

        # si llegó aquí, todas las producciones son regulares
        return True

    # Comprueba si la gramática es libre de contexto (Tipo 2).
    # Para ello cada LHS debe ser exactamente un no terminal.
    def es_glc(self):
        for A in self.producciones:
            if A not in self.no_terminales:
                return False
        return True

    # Clasifica la gramática según Chomsky de forma simple:
    # Tipo 3 -> Tipo 2 -> Tipo 1 (heurístico) -> Tipo 0
    def clasificar(self):
        if self.es_regular():
            return 'Tipo 3: Regular'
        if self.es_glc():
            return 'Tipo 2: Libre de Contexto'

        # Comprobación heurística para Tipo 1: si alguna producción
        # tiene ε o acorta la RHS respecto al LHS, no es Tipo 1
        es_tipo_1 = True
        for A, rhss in self.producciones.items():
            for r in rhss:
                if r == 'ε' or len(r) < len(A):
                    es_tipo_1 = False
                    break
            if not es_tipo_1:
                break

        if es_tipo_1:
            return 'Tipo 1: Sensible al contexto (aprox.)'

        return 'Tipo 0: Tipo libre (no restringida)'

    # Representación legible de la gramática
    def __str__(self):
        lines = []
        for A in sorted(self.producciones):
            rhss = ' | '.join(self.producciones[A])
            lines.append(f"{A} -> {rhss}")
        return '\n'.join(lines)
