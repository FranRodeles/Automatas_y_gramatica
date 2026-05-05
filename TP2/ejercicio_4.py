'''
Expresión regular: (a | b)*(a | b | ε)
Autómata Finito No-determinista (AFN) que acepta cadenas con:
  - Cero o más (a o b): (a | b)*
  - Seguido de opcionalmente (a, b, o nada): (a | b | ε)
'''

from collections import defaultdict, deque

# Definición del AFN
# Estado inicial: 0, Estado final: qf
# Alfabeto: {a, b}
AFN = {
    'estados': {0, 1, 2, 3, 4, 5, 6, 7, 8, 'qf'},
    'alfabeto': {'a', 'b'},
    'estado_inicial': 0,
    'estados_finales': {'qf'},
    'transiciones': defaultdict(lambda: defaultdict(set))
}

# Construcción de transiciones para la expresión regular (a | b)*(a | b | ε)
# Formato: AFN['transiciones'][estado_origen][símbolo].add(estado_destino)
#Un estado puede tener varias transiciones para el mismo símbolo

AFN['transiciones'][0]['ε'].add(1)      # Inicio: del 0 vamos al 1 sin leer nada

# Desde 1 hay 3 opciones (no-determinismo):
AFN['transiciones'][1]['ε'].add(2)      # Opción 1: para leer 'a'
AFN['transiciones'][1]['ε'].add(4)      # Opción 2: para leer 'b'
AFN['transiciones'][1]['ε'].add(7)      # Opción 3: para terminar (sin leer más)
# AFN['transiciones'][1]['ε'] = {2, 4, 7}

# Rama para leer 'a' en el ciclo (a|b)*
AFN['transiciones'][2]['a'].add(3)      # Leemos 'a'
AFN['transiciones'][3]['ε'].add(6)      # Vamos al punto de decisión

# Rama para leer 'b' en el ciclo (a|b)*
AFN['transiciones'][4]['b'].add(5)      # Leemos 'b'
AFN['transiciones'][5]['ε'].add(6)      # Vamos al punto de decisión

# Ciclo: después de leer a o b, podemos repetir o terminar
AFN['transiciones'][6]['ε'].add(1)      # Volver a leer más (a|b)
AFN['transiciones'][6]['ε'].add(7)      # O salir del ciclo

# Última etapa: (a | b | ε)
AFN['transiciones'][7]['ε'].add(8)      # Preparamos la lectura final
AFN['transiciones'][8]['a'].add('qf')   # Opción 1: leemos 'a' y aceptamos
AFN['transiciones'][8]['b'].add('qf')   # Opción 2: leemos 'b' y aceptamos
AFN['transiciones'][8]['ε'].add('qf')   # Opción 3: no leemos nada y aceptamos


def clausura_epsilon(estados, transiciones):
    """
    Calcula el cierre-ε: todos los estados alcanzables desde 'estados' 
    usando solo transiciones ε (sin leer caracteres).
    
    Algoritmo:
    1. Comenzar con los estados dados
    2. Para cada estado, buscar todas las transiciones ε
    3. Agregar esos nuevos estados a la clausura
    4. Repetir hasta que no haya más estados nuevos
    """
    pila = deque(estados) # Ver que estados faltan revisar
    clausura = set(estados) #Guarda el conjunto final
    
    while pila:
        estado_actual = pila.popleft()
        # Buscar todos los destinos por transición ε
        for estado_siguiente in transiciones[estado_actual].get('ε', set()):
            # Si no lo hemos visto, agregarlo
            if estado_siguiente not in clausura:
                clausura.add(estado_siguiente)
                pila.append(estado_siguiente)
    
    return clausura


def mover(estados, simbolo, transiciones):
    """
    Calcula: si estamos en 'estados' y leemos 'simbolo', 
    ¿a qué nuevos estados podemos ir? (sin aplicar cierre-ε)
    
    Algoritmo:
    1. Para cada estado actual
    2. Buscar dónde va con el símbolo leído
    3. Agregar todos esos destinos
    """
    resultado = set()
    for estado in estados:
        resultado.update(transiciones[estado].get(simbolo, set()))
    return resultado


def validar_cadena(cadena, afn):
    """
    Proceso:
    1. Verificar que todos los caracteres están en el alfabeto
    2. Comenzar en el estado inicial con su cierre-ε
    3. Para cada carácter:
       a. Mover a nuevos estados con ese carácter
       b. Calcular el cierre-ε de esos estados
    4. Aceptar si terminamos en un estado final
    """
    # Rechazar si hay caracteres inválidos
    if any(simbolo not in afn['alfabeto'] for simbolo in cadena):
        return False
    
    # Comenzar en estado inicial + cualquier estado alcanzable por ε
    estados_actuales = clausura_epsilon({afn['estado_inicial']}, afn['transiciones'])
    # Procesar cada caractér de la cadena
    for simbolo in cadena:
        # Mover según el símbolo
        estados_siguientes = mover(estados_actuales, simbolo, afn['transiciones'])
        # Aplicar cierre-ε a donde llegamos
        estados_actuales = clausura_epsilon(estados_siguientes, afn['transiciones'])
    
    # Aceptamos si terminamos en algún estado final
    return any(e in afn['estados_finales'] for e in estados_actuales)



if __name__ == '__main__':    
    # Pruebas con cadenas
    print('VALIDACIÓN DE CADENAS:')
    cadenas_prueba = ["", "a", "b", "ab", "ba", "aabb", "abc", "aab", "bba", "c", "aba"]
    for cadena in cadenas_prueba:
        resultado = validar_cadena(cadena, AFN)
        estado = 'Válida' if resultado else 'Inválida'
        print(f'  "{cadena:6}" → {estado}')

