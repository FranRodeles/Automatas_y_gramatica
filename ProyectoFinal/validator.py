"""Etapa 4: Validacion estructural con gramatica libre de contexto."""

from tokenizer import tokenize_message


def reduce_tokens_for_cfg(tokens: list[str]) -> list[str]:
    """Reduce tokens de la etapa 2 al alfabeto terminal de la etapa 4.

    Terminales de la gramatica: ``caps``, ``money``, ``contact``, ``text``.

    Reglas de reduccion:
    - ``CAPS`` -> ``caps``
    - ``MONEY`` -> ``money``
    - ``PHONE`` o ``URL`` -> ``contact``
    - uno o mas ``WORD`` consecutivos -> ``text``

    Args:
        tokens: Lista de tipos de token de la etapa 2.

    Returns:
        Lista de terminales reducidos para parseo CFG.
    """
    reduced: list[str] = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == "CAPS":
            reduced.append("caps")
            i += 1
            continue

        if token == "MONEY":
            reduced.append("money")
            i += 1
            continue

        if token in {"PHONE", "URL"}:
            reduced.append("contact")
            i += 1
            continue

        if token == "WORD":
            while i < len(tokens) and tokens[i] == "WORD":
                i += 1
            reduced.append("text")
            continue

        i += 1

    return reduced


def validate_spam_structure(reduced_tokens: list[str]) -> bool:
    """Valida la estructura de spam segun la GLC acordada.

    Gramatica usada:

    - ``S -> Hook Content Close``
    - ``Hook -> caps Hook | caps``
    - ``Content -> Piece Content | Piece``
    - ``Piece -> money | text``
    - ``Close -> contact Close | contact``

    Equivalente operacional:
    1) uno o mas ``caps``
    2) uno o mas ``money`` o ``text``
    3) uno o mas ``contact``
    4) sin simbolos extra al final.

    Args:
        reduced_tokens: Secuencia reducida al alfabeto terminal de etapa 4.

    Returns:
        ``True`` si la secuencia deriva desde ``S``, ``False`` en caso contrario.
    """
    if not reduced_tokens:
        return False

    i = 0
    n = len(reduced_tokens)

    if reduced_tokens[i] != "caps":
        return False
    while i < n and reduced_tokens[i] == "caps":
        i += 1

    if i >= n or reduced_tokens[i] not in {"money", "text"}:
        return False
    while i < n and reduced_tokens[i] in {"money", "text"}:
        i += 1

    if i >= n or reduced_tokens[i] != "contact":
        return False
    while i < n and reduced_tokens[i] == "contact":
        i += 1

    return i == n


def validate_message_structure(message: str) -> tuple[bool, list[str], list[str]]:
    """Tokeniza, reduce y valida estructuralmente un mensaje completo.

    Args:
        message: Mensaje original.

    Returns:
        Tupla ``(es_valido, tokens_etapa2, tokens_reducidos)``.
    """
    tokens = tokenize_message(message)
    reduced = reduce_tokens_for_cfg(tokens)
    return validate_spam_structure(reduced), tokens, reduced
