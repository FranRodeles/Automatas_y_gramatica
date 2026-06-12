"""Etapa 3: Clasificador heurístico basado en pesos predictivos."""

import os
import csv
from tokenizer import tokenize_message


# Punto de ajuste 1:
# Modifica estos valores para cambiar el peso de cada tipo de token.
# El score final de un mensaje es la suma de estos pesos.
WEIGHTS = {
    "MONEY": 3,
    "PHONE": 3,
    "URL": 2,
    "CAPS": 1,
    "WORD": 0,
}


def calculate_message_score(tokens: list[str]) -> int:
    """Calcula la puntuación total de un mensaje sumando los pesos de sus tokens.

    Args:
        tokens: Lista de tipos de tokens obtenidos de la Etapa 2.

    Returns:
        Suma total de los pesos de los tokens presentes.
    """
    return sum(WEIGHTS.get(token, 0) for token in tokens)


def classify_message(tokens: list[str], threshold: int) -> str:
    """Clasifica un mensaje como SPAM o HAM basándose en un umbral de peso.

    Args:
        tokens: Lista de tipos de tokens obtenidos de la Etapa 2.
        threshold: Umbral (U) para determinar si el mensaje es spam.

    Returns:
        "SPAM" si la puntuación supera el umbral, "HAM" en caso contrario.
    """
    score = calculate_message_score(tokens)
    # Punto de ajuste 2:
    # Regla de decisión actual: SPAM solo si score > threshold.
    # Si quieres una regla más estricta o más flexible, cambia esta línea.
    # Ejemplo: usar ">=" en lugar de ">".
    return "SPAM" if score > threshold else "HAM"


def evaluate_accuracy(csv_path: str, threshold: int, sample_size: int = 100) -> float:
    """Evalúa la precisión (Accuracy) del clasificador sobre un dataset.

    Args:
        csv_path: Ruta al archivo CSV con los datos (columnas: text, label).
        threshold: Umbral (U) a evaluar.
        sample_size: Número de mensajes a evaluar (por defecto 100).

    Returns:
        Proporción de predicciones correctas (0.0 a 1.0).
    """
    correct_predictions = 0
    processed_count = 0

    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if processed_count >= sample_size:
                    break

                text = row["text"]
                # El label es '0' para HAM y '1' para SPAM
                actual_label = "SPAM" if row["label"] == "1" else "HAM"

                tokens = tokenize_message(text)
                prediction = classify_message(tokens, threshold)

                if prediction == actual_label:
                    correct_predictions += 1
                processed_count += 1
    except FileNotFoundError:
        print(f"Error: Archivo {csv_path} no encontrado.")
        return 0.0

    return correct_predictions / processed_count if processed_count > 0 else 0.0


def formal_definition() -> str:
    """Devuelve la definición formal de la Etapa 3.

    Returns:
        Definición textual del modelo de pesos y criterio de decisión.
    """
    weights_str = ", ".join([f"{k}: {v}" for k, v in WEIGHTS.items()])
    return (
        "Etapa 3: Clasificador Heurístico por Pesos.\n"
        f"Pesos: {weights_str}\n"
        "Criterio: Si Score(mensaje) > U, entonces SPAM; sino, HAM."
    )


def main() -> None:
    """Ejecuta la evaluación de la Etapa 3 con diferentes umbrales."""
    # Obtener la ruta absoluta del archivo CSV relativa al script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "SpamCollectionSpanish.csv")
    # Punto de ajuste 3:
    # Lista de umbrales U a evaluar para elegir el mejor.
    thresholds_to_test = [2, 5, 10]

    print(formal_definition())
    print("\nEvaluando precisión sobre 100 mensajes...")
    print("-" * 40)

    results: dict[int, float] = {}
    for u in thresholds_to_test:
        accuracy = evaluate_accuracy(dataset_path, u)
        results[u] = accuracy
        print(f"Umbral U = {u:2} | Accuracy: {accuracy:.2%}")

    print("-" * 40)
    best_u = max(results, key=lambda k: results[k])
    print(f"Conclusion: El mejor umbral es U = {best_u} con una precision de {results[best_u]:.2%}")


if __name__ == "__main__":
    main()
