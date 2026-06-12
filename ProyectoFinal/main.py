"""Pipeline principal: lectura de CSV y ejecucion de etapas 1, 2 y 3."""

import csv
import os

from classifier import classify_message
from tokenizer import tokenize_normalized_text
from turing import normalize_message
from validator import reduce_tokens_for_cfg, validate_spam_structure


def run_pipeline(csv_path: str, threshold: int = 5) -> tuple[int, dict[str, object] | None]:
    """Lee el CSV completo y procesa cada mensaje por las 3 etapas.

    Args:
        csv_path: Ruta al CSV con columnas ``text`` y ``label``.
        threshold: Umbral para la etapa 3 (clasificacion).

    Returns:
        Cantidad de mensajes procesados y una muestra de salida para revision.
    """
    processed = 0
    sample: dict[str, object] | None = None

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row["text"]

            normalized_text = normalize_message(text)
            tokens = tokenize_normalized_text(normalized_text)
            prediction = classify_message(tokens, threshold)

            if sample is None:
                actual_label = "SPAM" if row.get("label") == "1" else "HAM"
                sample = {
                    "text": text,
                    "normalized_text": normalized_text,
                    "tokens": tokens,
                    "prediction": prediction,
                    "actual_label": actual_label,
                }

            processed += 1

    return processed, sample


def build_stage3_comparison_csv(
    input_csv_path: str,
    output_csv_path: str,
    thresholds: list[int],
) -> tuple[int, dict[int, int]]:
    """Genera un CSV comparativo de etapa 3 para multiples umbrales U.

    El archivo incluye la etiqueta original y las predicciones binarias por U.

    Args:
        input_csv_path: Ruta del CSV original (columnas ``text``, ``label``).
        output_csv_path: Ruta del CSV de salida comparativo.
        thresholds: Lista de valores de umbral U.

    Returns:
        Cantidad de filas procesadas y aciertos por umbral U.
    """
    messages: list[dict[str, str]] = []

    with open(input_csv_path, mode="r", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            messages.append(row)

    binary_predictions_by_u: dict[int, list[int]] = {}
    for u in thresholds:
        predictions: list[int] = []
        for row in messages:
            tokens = tokenize_normalized_text(normalize_message(row["text"]))
            label = classify_message(tokens, u)
            predictions.append(1 if label == "SPAM" else 0)
        binary_predictions_by_u[u] = predictions

    correct_by_u: dict[int, int] = {u: 0 for u in thresholds}

    with open(output_csv_path, mode="w", encoding="utf-8", newline="") as output_file:
        fieldnames = ["original"]
        for u in thresholds:
            fieldnames.append(f"pred_u_{u}")
            fieldnames.append(f"ok_u_{u}")
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for index, row in enumerate(messages):
            original = int(row["label"])
            out_row = {"original": original}
            for u in thresholds:
                prediction = binary_predictions_by_u[u][index]
                ok = 1 if prediction == original else 0
                out_row[f"pred_u_{u}"] = prediction
                out_row[f"ok_u_{u}"] = ok
                correct_by_u[u] += ok
            writer.writerow(out_row)

    return len(messages), correct_by_u


def build_accuracy_summary_csv(
    output_csv_path: str,
    total_rows: int,
    correct_by_u: dict[int, int],
) -> None:
    """Genera un resumen de aciertos por umbral U.

    Args:
        output_csv_path: Ruta del CSV resumen.
        total_rows: Cantidad total de mensajes evaluados.
        correct_by_u: Diccionario con aciertos por cada U.
    """
    with open(output_csv_path, mode="w", encoding="utf-8", newline="") as output_file:
        fieldnames = ["u", "aciertos", "total", "accuracy"]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for u in sorted(correct_by_u):
            hits = correct_by_u[u]
            accuracy = hits / total_rows if total_rows else 0.0
            writer.writerow(
                {
                    "u": u,
                    "aciertos": hits,
                    "total": total_rows,
                    "accuracy": f"{accuracy:.6f}",
                }
            )


def build_stage4_exceptions_csv(
    input_csv_path: str,
    output_csv_path: str,
    thresholds: list[int],
) -> int:
    """Genera un CSV de excepciones de etapa 4 para cada umbral U.

    Una excepcion es un mensaje etiquetado como SPAM en etapa 3 que no cumple
    la validacion estructural de etapa 4.

    Args:
        input_csv_path: Ruta del CSV original (columnas ``text``, ``label``).
        output_csv_path: Ruta del CSV de salida con excepciones.
        thresholds: Lista de valores de umbral U.

    Returns:
        Cantidad total de excepciones registradas.
    """
    rows: list[dict[str, str]] = []

    with open(input_csv_path, mode="r", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            rows.append(row)

    exception_count = 0
    with open(output_csv_path, mode="w", encoding="utf-8", newline="") as output_file:
        fieldnames = [
            "u",
            "index",
            "original",
            "predicted_stage3",
            "stage4_valid",
            "reduced_tokens",
            "text",
        ]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for u in thresholds:
            for index, row in enumerate(rows):
                text = row["text"]
                tokens = tokenize_normalized_text(normalize_message(text))
                predicted = classify_message(tokens, u)
                if predicted != "SPAM":
                    continue

                reduced = reduce_tokens_for_cfg(tokens)
                stage4_valid = validate_spam_structure(reduced)

                if stage4_valid:
                    continue

                writer.writerow(
                    {
                        "u": u,
                        "index": index,
                        "original": int(row["label"]),
                        "predicted_stage3": 1,
                        "stage4_valid": 0,
                        "reduced_tokens": " ".join(reduced),
                        "text": text,
                    }
                )
                exception_count += 1

    return exception_count


def main() -> None:
    """Ejecuta el pipeline completo sobre el CSV del proyecto."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, "SpamCollectionSpanish.csv")
    stage3_output = os.path.join(script_dir, "stage3_comparacion.csv")
    accuracy_summary_output = os.path.join(script_dir, "aciertos_resumen.csv")
    stage4_exceptions_output = os.path.join(script_dir, "excepcion.csv")
    thresholds = [2, 5, 10]

    total, sample = run_pipeline(dataset_path)
    print(f"Mensajes procesados por etapas 1-2-3: {total}")

    if sample is not None:
        print("\nMuestra de verificacion (1 mensaje):")
        print(f"Texto original: {sample['text']}")
        print(f"Texto normalizado: {sample['normalized_text']}")
        print(f"Tokens: {sample['tokens']}")
        print(f"Clasificacion: {sample['prediction']}")
        print(f"Etiqueta real: {sample['actual_label']}")

    compared_rows, correct_by_u = build_stage3_comparison_csv(
        input_csv_path=dataset_path,
        output_csv_path=stage3_output,
        thresholds=thresholds,
    )
    build_accuracy_summary_csv(
        output_csv_path=accuracy_summary_output,
        total_rows=compared_rows,
        correct_by_u=correct_by_u,
    )
    print(f"\nCSV comparativo de etapa 3 creado: {stage3_output}")
    print(f"Filas comparadas (original + U): {compared_rows}")
    print(f"CSV resumen de aciertos creado: {accuracy_summary_output}")
    for u in thresholds:
        hits = correct_by_u[u]
        accuracy = hits / compared_rows if compared_rows else 0.0
        print(f"U={u}: {hits}/{compared_rows} aciertos ({accuracy:.2%})")

    exception_rows = build_stage4_exceptions_csv(
        input_csv_path=dataset_path,
        output_csv_path=stage4_exceptions_output,
        thresholds=thresholds,
    )
    print(f"CSV de excepciones de etapa 4 creado: {stage4_exceptions_output}")
    print(f"Excepciones detectadas (SPAM etapa 3 no valido en etapa 4): {exception_rows}")


if __name__ == "__main__":
    main()
