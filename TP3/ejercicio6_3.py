'''
Punto 6.3 - Parser Descendente Recursivo

Gramatica:
    E  -> T E'
    E' -> + T E' | ε
    T  -> F T'
    T' -> * F T' | ε
    F  -> ( E ) | num
'''

import re
import sys


# Permite imprimir correctamente el simbolo ε en consolas de Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class ParserDescendente:
    PATRONES_VALIDOS = (r'num', r'\+', r'\*', r'\(', r'\)')

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def parsear(self):
        """Inicia el analisis sintactico desde el simbolo inicial E."""
        self._validar_tokens()
        self._E()

        # Si queda algun token sin consumir, la expresion no pertenece a la gramatica.
        if self._token_actual() is not None:
            self._error("fin de cadena")

        print("Resultado: ACEPTADO")
        return True

    def _validar_tokens(self):
        for token in self.tokens:
            if not any(re.fullmatch(patron, token) for patron in self.PATRONES_VALIDOS):
                raise SyntaxError(f"Token invalido: '{token}'")

    def _token_actual(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return None

    def _avanzar(self):
        self.posicion += 1

    def _coincidir(self, patron, esperado):
        """Consume el token actual solo si coincide con el patron esperado."""
        token = self._token_actual()

        if token is not None and re.fullmatch(patron, token):
            self._avanzar()
            return

        self._error(esperado)

    def _error(self, esperado):
        encontrado = self._token_actual()
        if encontrado is None:
            encontrado = "fin de cadena"

        raise SyntaxError(
            f"Error sintactico: se esperaba {esperado}, se encontro '{encontrado}'"
        )

    def _E(self):
        print("Aplicando E -> T E'")
        self._T()
        self._E_prima()

    def _E_prima(self):
        token = self._token_actual()

        if token is not None and re.fullmatch(r'\+', token):
            print("Aplicando E' -> + T E'")
            self._coincidir(r'\+', "'+'")
            self._T()
            self._E_prima()
        else:
            # E' puede desaparecer cuando no viene un '+'.
            print("Aplicando E' -> ε")

    def _T(self):
        print("Aplicando T -> F T'")
        self._F()
        self._T_prima()

    def _T_prima(self):
        token = self._token_actual()

        if token is not None and re.fullmatch(r'\*', token):
            print("Aplicando T' -> * F T'")
            self._coincidir(r'\*', "'*'")
            self._F()
            self._T_prima()
        else:
            # T' puede desaparecer cuando no viene un '*'.
            print("Aplicando T' -> ε")

    def _F(self):
        token = self._token_actual()

        # F es el unico no terminal que consume 'num' o una expresion entre parentesis.
        if token is not None and re.fullmatch(r'num', token):
            print("Aplicando F -> num")
            self._coincidir(r'num', "'num'")
        elif token is not None and re.fullmatch(r'\(', token):
            print("Aplicando F -> ( E )")
            self._coincidir(r'\(', "'('")
            self._E()
            self._coincidir(r'\)', "')'")
        else:
            self._error("'num' o '('")


def probar_cadena(tokens):
    print(f"Tokens: {tokens}")
    parser = ParserDescendente(tokens)

    try:
        parser.parsear()
    except SyntaxError as error:
        print(error)

    print("\n------------------------------\n")


if __name__ == "__main__":
    pruebas = [
        ['num'],
        ['num', '+', 'num', '*', 'num'],
        ['(', 'num', '+', 'num', ')', '*', 'num'],
        ['num', '+', '+', 'num'],
        ['num', '*'],
        ['(', 'num', '+', 'num'],
    ]

    for tokens_prueba in pruebas:
        probar_cadena(tokens_prueba)
