#!/usr/bin/env python3
"""
Script d'évaluation pour le benchmark d'analyse rhétorique.

Compare les annotations du modèle avec les annotations de référence (gold standard)
et calcule des métriques de performance.

Usage:
    python evaluate.py gold.json predicted.json
    python evaluate.py --batch benchmark/annotations/gold/ benchmark/annotations/model/
"""

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EvaluationMetrics:
    """Métriques d'évaluation pour une analyse."""

    # Détection de sophismes
    fallacy_precision: float = 0.0
    fallacy_recall: float = 0.0
    fallacy_f1: float = 0.0
    fallacy_details: dict[str, dict[str, float]] = field(default_factory=dict)

    # Score de fiabilité
    reliability_mae: float = 0.0  # Mean Absolute Error
    reliability_correlation: float = 0.0

    # Nombre d'arguments
    argument_count_gold: int = 0
    argument_count_predicted: int = 0

    # Composants Toulmin (si annotés)
    toulmin_claim_match: float = 0.0
    toulmin_grounds_match: float = 0.0

    def to_dict(self) -> dict:
        return {
            "fallacy_precision": round(self.fallacy_precision, 3),
            "fallacy_recall": round(self.fallacy_recall, 3),
            "fallacy_f1": round(self.fallacy_f1, 3),
            "reliability_mae": round(self.reliability_mae, 3),
            "argument_count_gold": self.argument_count_gold,
            "argument_count_predicted": self.argument_count_predicted,
        }


def extract_fallacies(analysis: dict) -> dict[int, list[str]]:
    """Extrait les sophismes par argument."""
    result = {}
    for arg in analysis.get("arguments", []):
        arg_id = arg.get("id", 0)
        fallacies = arg.get("fallacies", [])
        # Normaliser les noms de sophismes (lowercase, sans espaces)
        normalized = [f.lower().strip().replace(" ", "_") for f in fallacies if f]
        result[arg_id] = normalized
    return result


def extract_reliability_scores(analysis: dict) -> dict[int, int]:
    """Extrait les scores de fiabilité par argument."""
    result = {}
    for arg in analysis.get("arguments", []):
        arg_id = arg.get("id", 0)
        reliability = arg.get("reliability", 3)
        result[arg_id] = reliability
    return result


def compute_fallacy_metrics(
    gold_fallacies: dict[int, list[str]], pred_fallacies: dict[int, list[str]]
) -> tuple[float, float, float, dict]:
    """
    Calcule precision, recall, F1 pour la détection de sophismes.

    On considère une détection correcte si:
    - Le même argument est identifié
    - Le même type de sophisme est détecté
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    details_by_type = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    # Aligner par argument ID
    all_arg_ids = set(gold_fallacies.keys()) | set(pred_fallacies.keys())

    for arg_id in all_arg_ids:
        gold_set = set(gold_fallacies.get(arg_id, []))
        pred_set = set(pred_fallacies.get(arg_id, []))

        # True positives: dans gold ET dans pred
        tp = gold_set & pred_set
        true_positives += len(tp)
        for f in tp:
            details_by_type[f]["tp"] += 1

        # False positives: dans pred mais pas dans gold
        fp = pred_set - gold_set
        false_positives += len(fp)
        for f in fp:
            details_by_type[f]["fp"] += 1

        # False negatives: dans gold mais pas dans pred
        fn = gold_set - pred_set
        false_negatives += len(fn)
        for f in fn:
            details_by_type[f]["fn"] += 1

    # Calcul des métriques globales
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0
    )
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    # Calcul par type
    details = {}
    for fallacy_type, counts in details_by_type.items():
        tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]
        p = tp / (tp + fp) if (tp + fp) > 0 else 0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0
        f = 2 * p * r / (p + r) if (p + r) > 0 else 0
        details[fallacy_type] = {"precision": p, "recall": r, "f1": f}

    return precision, recall, f1, details


def compute_reliability_mae(gold_scores: dict[int, int], pred_scores: dict[int, int]) -> float:
    """Calcule le Mean Absolute Error sur les scores de fiabilité."""
    common_ids = set(gold_scores.keys()) & set(pred_scores.keys())

    if not common_ids:
        return 0.0

    total_error = sum(abs(gold_scores[i] - pred_scores[i]) for i in common_ids)
    return total_error / len(common_ids)


def evaluate_analysis(gold: dict, predicted: dict) -> EvaluationMetrics:
    """
    Évalue une analyse prédite par rapport à la référence gold.

    Args:
        gold: Annotation de référence (format JSON du skill)
        predicted: Annotation du modèle

    Returns:
        EvaluationMetrics avec toutes les métriques calculées
    """
    metrics = EvaluationMetrics()

    # Nombre d'arguments
    metrics.argument_count_gold = len(gold.get("arguments", []))
    metrics.argument_count_predicted = len(predicted.get("arguments", []))

    # Extraction des données
    gold_fallacies = extract_fallacies(gold)
    pred_fallacies = extract_fallacies(predicted)

    gold_reliability = extract_reliability_scores(gold)
    pred_reliability = extract_reliability_scores(predicted)

    # Calcul des métriques de sophismes
    precision, recall, f1, details = compute_fallacy_metrics(gold_fallacies, pred_fallacies)
    metrics.fallacy_precision = precision
    metrics.fallacy_recall = recall
    metrics.fallacy_f1 = f1
    metrics.fallacy_details = details

    # Calcul du MAE sur la fiabilité
    metrics.reliability_mae = compute_reliability_mae(gold_reliability, pred_reliability)

    return metrics


def print_report(metrics: EvaluationMetrics, verbose: bool = True) -> None:
    """Affiche un rapport formaté des métriques."""
    print("\n" + "=" * 60)
    print("RAPPORT D'ÉVALUATION")
    print("=" * 60)

    print("\n📊 Arguments identifiés:")
    print(f"   Gold: {metrics.argument_count_gold}")
    print(f"   Modèle: {metrics.argument_count_predicted}")

    print("\n🎯 Détection de sophismes:")
    print(f"   Precision: {metrics.fallacy_precision:.2%}")
    print(f"   Recall: {metrics.fallacy_recall:.2%}")
    print(f"   F1: {metrics.fallacy_f1:.2%}")

    if verbose and metrics.fallacy_details:
        print("\n   Détail par type:")
        for fallacy_type, scores in sorted(metrics.fallacy_details.items()):
            print(
                f"   - {fallacy_type}: P={scores['precision']:.2f} R={scores['recall']:.2f} F1={scores['f1']:.2f}"
            )

    print("\n📏 Score de fiabilité:")
    print(f"   MAE: {metrics.reliability_mae:.2f} (sur échelle 1-5)")

    # Interprétation
    print("\n" + "-" * 60)
    print("INTERPRÉTATION:")
    if metrics.fallacy_f1 >= 0.7:
        print("✅ Bonne détection des sophismes")
    elif metrics.fallacy_f1 >= 0.5:
        print("⚠️  Détection des sophismes à améliorer")
    else:
        print("❌ Détection des sophismes insuffisante")

    if metrics.reliability_mae <= 0.5:
        print("✅ Scores de fiabilité bien calibrés")
    elif metrics.reliability_mae <= 1.0:
        print("⚠️  Scores de fiabilité à affiner")
    else:
        print("❌ Scores de fiabilité à recalibrer")

    print("=" * 60 + "\n")


def batch_evaluate(gold_dir: Path, pred_dir: Path) -> list[tuple[str, EvaluationMetrics]]:
    """Évalue tous les fichiers d'un répertoire."""
    results = []

    for gold_file in gold_dir.glob("*.json"):
        pred_file = pred_dir / gold_file.name
        if pred_file.exists():
            with open(gold_file) as f:
                gold = json.load(f)
            with open(pred_file) as f:
                pred = json.load(f)

            metrics = evaluate_analysis(gold, pred)
            results.append((gold_file.stem, metrics))
        else:
            print(f"⚠️  Pas de prédiction pour {gold_file.name}")

    return results


def export_results_csv(results: list[tuple[str, EvaluationMetrics]], output_path: Path) -> None:
    """Exporte les résultats en CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "article",
                "fallacy_precision",
                "fallacy_recall",
                "fallacy_f1",
                "reliability_mae",
                "arg_count_gold",
                "arg_count_pred",
            ]
        )
        for name, metrics in results:
            writer.writerow(
                [
                    name,
                    f"{metrics.fallacy_precision:.3f}",
                    f"{metrics.fallacy_recall:.3f}",
                    f"{metrics.fallacy_f1:.3f}",
                    f"{metrics.reliability_mae:.3f}",
                    metrics.argument_count_gold,
                    metrics.argument_count_predicted,
                ]
            )
    print(f"✅ Résultats exportés dans {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Évaluation d'analyses rhétoriques")
    parser.add_argument("gold", help="Fichier/répertoire gold standard")
    parser.add_argument("predicted", help="Fichier/répertoire des prédictions")
    parser.add_argument("--batch", action="store_true", help="Mode batch (répertoires)")
    parser.add_argument("--output", "-o", help="Fichier CSV de sortie (mode batch)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Mode silencieux")

    args = parser.parse_args()

    if args.batch:
        gold_dir = Path(args.gold)
        pred_dir = Path(args.predicted)

        results = batch_evaluate(gold_dir, pred_dir)

        if not args.quiet:
            print(f"\n📁 Évaluation de {len(results)} fichiers\n")
            for name, metrics in results:
                print(f"--- {name} ---")
                print_report(metrics, verbose=False)

        if args.output:
            export_results_csv(results, Path(args.output))

        # Moyennes globales
        if results:
            avg_f1 = sum(m.fallacy_f1 for _, m in results) / len(results)
            avg_mae = sum(m.reliability_mae for _, m in results) / len(results)
            print("\n📊 MOYENNES GLOBALES:")
            print(f"   Fallacy F1: {avg_f1:.2%}")
            print(f"   Reliability MAE: {avg_mae:.2f}")
    else:
        with open(args.gold) as f:
            gold = json.load(f)
        with open(args.predicted) as f:
            predicted = json.load(f)

        metrics = evaluate_analysis(gold, predicted)

        if not args.quiet:
            print_report(metrics)

        # Retour JSON pour intégration
        print(json.dumps(metrics.to_dict(), indent=2))


if __name__ == "__main__":
    main()
