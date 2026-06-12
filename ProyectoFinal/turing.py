"""Etapa 1: Normalizacion selectiva con Maquina de Turing."""

from typing import Dict, Iterable, List, Set, Tuple

from turing_machine import TuringMachine


Symbol = str
State = str
Direction = str
TransitionKey = Tuple[State, Symbol]
TransitionValue = Tuple[State, Symbol, Direction]


def build_normalizer_tm(extra_symbols: Iterable[Symbol] | None = None) -> TuringMachine:
    """Construye la MT de normalizacion

    La MT conserva letras, digitos, espacios y simbolos criticos: $ £ € . : /
    Cualquier otro simbolo se reemplaza por un espacio en la cinta.

    Returns:
        Instancia de TuringMachine configurada.
    """
    blank = ""
    critical_symbols = set("$£€.:/")
    accepted_symbols = set(
        "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        "abcdefghijklmnñopqrstuvwxyz"
        "ÁÉÍÓÚ"
        "áéíóú"
        "0123456789"
        " "
    ) | critical_symbols

    transitions: Dict[TransitionKey, TransitionValue] = {}

    def add_keep(symbols: Iterable[Symbol]) -> None:
        for symbol in symbols:
            transitions[("q0", symbol)] = ("q0", symbol, "R")

    add_keep(accepted_symbols)

    if extra_symbols is not None:
        for symbol in extra_symbols:
            if symbol not in accepted_symbols and symbol != blank:
                transitions[("q0", symbol)] = ("q0", blank, "R")

    transitions[("q0", blank)] = ("qa", blank, "R")

    return TuringMachine(
        transitions,
        start_state="q0",
        accept_state="qa",
        reject_state="qr",
        blank_symbol=blank,
    )


def normalize_message(message: str) -> str:
    """Normaliza un mensaje aplicando la MT de Etapa 1.

    Args:
        message: Mensaje de entrada.

    Returns:
        Mensaje normalizado.
    """
    tm = build_normalizer_tm(extra_symbols=message)
    tape = list(message) + [tm.blank_symbol]
    last_config = None

    for action, config in tm.run(tape):
        last_config = config
        if action is not None:
            break

    if last_config is None:
        return ""

    left = "".join(reversed(last_config["left_hand_side"]))
    right = "".join(last_config["right_hand_side"])
    current = last_config["symbol"]
    full_tape = f"{left}{current}{right}"
    return full_tape[: len(message)]


def trace_steps(message: str, step_limit: int = 200) -> List[str]:
    """Genera la traza completa de configuraciones (opcional).

    Args:
        message: Mensaje de entrada.
        step_limit: Limite de pasos para la traza.

    Returns:
        Lista de configuraciones en formato legible.
    """
    tm = build_normalizer_tm(extra_symbols=message)
    steps: List[str] = []
    for action, config in tm.run(list(message) + [tm.blank_symbol]):
        left = "".join(reversed(config["left_hand_side"]))
        right = "".join(config["right_hand_side"])
        state = config["state"]
        symbol = config["symbol"]
        steps.append(f"{state} | {left}[{symbol}]{right}")
        if action is not None:
            break
        if len(steps) >= step_limit:
            break
    return steps


def formal_definition() -> str:
    """Devuelve la definicion formal de la MT en formato textual.

    Returns:
        Definicion formal (Q, Sigma, Gamma, delta, q0, F).
    """
    q_set = "{q0, qa, qr}"
    sigma_accepted = "{letras, digitos, espacio, $, £, €, ., :, /}"
    sigma_rejected = "{cualquier otro simbolo}"
    gamma_set = "{letras, digitos, espacio, $, £, €, ., :, /, blanco}"

    lines = [
        "M = (Q, Sigma, Gamma, delta, q0, F)",
        f"Q = {q_set}",
        f"Sigma (aceptado) = {sigma_accepted}",
        f"Sigma (no aceptado) = {sigma_rejected}",
        f"Gamma = {gamma_set}",
        "delta: (q0, x) -> (q0, x, R) si x es aceptado",
        "delta: (q0, x) -> (q0, ' ', R) si x no es aceptado",
        "delta: (q0, blanco) -> (qa, blanco, R)",
        "q0 = q0",
        "F = {qa}",
    ]
    return "\n".join(lines)


def main() -> None:
    """Ejecuta la normalizacion con el ejemplo del enunciado."""
    message = "¡Llame al 09094100151 para usar sus minutos! Las llamadas se emiten a 10 p/min (la mafia varía). Servicio proporcionado por AOM, solo 5 GBP al mes. AOM Box61,M60 1ER hasta que te detengas. ¡Solo mayores de 18 años!"
    print(formal_definition())
    print("\nEntrada:")
    print(message)
    print("\nSalida normalizada:")
    print(normalize_message(message))

    # Para depuracion de la MT (traza completa), descomentar:
    # for step in trace_steps(message):
    #     print(step)


if __name__ == "__main__":
    main()
