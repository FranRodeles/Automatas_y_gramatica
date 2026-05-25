"""Etapa 2: Tokenizacion con expresiones regulares."""

import re

from turing import normalize_message


TOKEN_PATTERNS = {
    "MONEY": (
        r"(?:[$£€][0-9]+(?:\.[0-9]+)?|"
        r"[0-9]+(?:\.[0-9]+)?[$£€])"
    ),
    "URL": r"(?:https?://[A-Za-z0-9./]+|www\.[A-Za-z0-9.]+)",
    "PHONE": r"[0-9]{7,}",
    "CAPS": r"[A-Z]{3,}",
    "WORD": r"[A-Za-z0-9]+",
}

TOKEN_REGEX = re.compile(
    "|".join(
        f"(?P<{token_type}>{pattern})"
        for token_type, pattern in TOKEN_PATTERNS.items()
    )
)


def tokenize_normalized_text(normalized_text: str) -> list[str]:
    """Convierte texto normalizado en una lista ordenada de tipos de tokens.

    La funcion implementa un analizador lexico por expresiones regulares. El
    orden de los patrones es relevante: MONEY y URL deben reconocerse antes que
    PHONE, CAPS y WORD para evitar particiones parciales de un mismo lexema.

    Args:
        normalized_text: Cadena ya normalizada por la Maquina de Turing.

    Returns:
        Lista ordenada con los tipos de tokens encontrados.
    """
    token_types = []

    for match in TOKEN_REGEX.finditer(normalized_text):
        token_types.append(match.lastgroup)

    return token_types


def tokenize_message(message: str) -> list[str]:
    """Normaliza un mensaje con la MT y devuelve sus tipos de tokens.

    Args:
        message: Mensaje original a procesar.

    Returns:
        Lista ordenada de tipos de tokens producida por la etapa 2.
    """
    normalized_text = normalize_message(message)
    return tokenize_normalized_text(normalized_text)


def formal_definition() -> str:
    """Devuelve la definicion formal conceptual del lexer regular.

    Returns:
        Definicion textual de los lenguajes regulares usados en la etapa 2.
    """
    lines = [
        "Etapa 2: Lexer regular L = Lmoney U Lurl U Lphone U Lcaps U Lword",
        f"MONEY = {TOKEN_PATTERNS['MONEY']}",
        f"URL = {TOKEN_PATTERNS['URL']}",
        f"PHONE = {TOKEN_PATTERNS['PHONE']}",
        f"CAPS = {TOKEN_PATTERNS['CAPS']}",
        f"WORD = {TOKEN_PATTERNS['WORD']}",
        "Cada lenguaje es regular porque puede ser descrito por una ER finita.",
    ]
    return "\n".join(lines)


def main() -> None:
    """Ejecuta la tokenizacion con un ejemplo integral."""
    message = "WIN $1000 now! visit http://spam.com or call 1234567"
    normalized_text = normalize_message(message)

    print(formal_definition())
    print("\nEntrada:")
    print(message)
    print("\nSalida normalizada:")
    print(normalized_text)
    print("\nTipos de tokens:")
    print(", ".join(tokenize_normalized_text(normalized_text)))


if __name__ == "__main__":
    main()
