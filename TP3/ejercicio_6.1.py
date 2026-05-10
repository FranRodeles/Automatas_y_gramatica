'''
	Implemente una clase Gramatica que represente una gramática formal y que permita
	realizar operaciones básicas.
	La clase debe incluir al menos:
	• Constructor: recibe terminales, no terminales, símbolo inicial y producciones.
	• clasificar(): retorna el tipo de gramática según la jerarquía de Chomsky (0, 1, 2 o 3).
	• es_regular(): retorna True si la gramática es de Tipo 3.
	• es_glc(): retorna True si la gramática es de Tipo 2.
	• __str__(): muestra la gramática de forma legible. 
	# Gramática para a^n b^n
	g = Gramatica(
	 terminales={'a', 'b'},
	 no_terminales={'S'},
	 simbolo_inicial='S',
	 producciones={'S': ['aSb', 'ε']}
	)
	print(g.clasificar()) # → 'Tipo 2: Libre de Contexto'
	print(g.es_regular()) # → False
	print(g.es_glc()) # → True
	print(g) # → muestra las producciones

	Además, implemente una función cargar_desde_texto(texto) que permita cargar
	una gramática desde un string con el siguiente formato:
	texto = "S -> aSb | ε"

	g = cargar_desde_texto(texto)
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


def cargar_desde_texto(texto):
	# Carga una gramática desde un string en formato: S -> aSb | ε
	# Infiere los no terminales (símbolos mayúsculas) y terminales
	producciones = {}
	no_terminales = set()
	terminales = set()

	for raw in texto.splitlines():
		linea = raw.strip()
		# saltamos líneas vacías o comentarios
		if not linea or linea.startswith('#'):
			continue

		# verificamos que tenga el formato LHS -> RHS
		if '->' not in linea:
			continue

		# separamos LHS y RHS
		lhs, rhs = linea.split('->', 1)
		lhs = lhs.strip()
		# el LHS es un no-terminal
		no_terminales.add(lhs)
		# el RHS puede tener alternativas separadas por |
		alternativas = [alt.strip() for alt in rhs.split('|')]
		producciones.setdefault(lhs, [])
		for alt in alternativas:
			producciones[lhs].append(alt)
			if alt != 'ε':
				# extraemos caracteres individuales para inferir NT y terminales
				for ch in alt:
					if ch.isupper():
						no_terminales.add(ch)
					else:
						terminales.add(ch)

	# el símbolo inicial es la primera LHS
	simbolo_inicial = next(iter(producciones)) if producciones else ''
    # Devuelve un objeto Gramatica con los conjuntos y producciones inferidos
	return Gramatica(terminales=terminales, no_terminales=no_terminales, simbolo_inicial=simbolo_inicial, producciones=producciones)


if __name__ == '__main__':
    # Ejemplo de uso sencillo: gramática para a^n b^n (no regular, sí libre de contexto)
    texto = 'S -> aSb | ε'
    g = cargar_desde_texto(texto)
    print('Producciones:')
    print(g)
    print('Clasificación:', g.clasificar())
    print('Es regular?', g.es_regular())
    print('Es GLC?', g.es_glc())






