#!/usr/bin/env python3
"""
Générateur de tableau d'analyse rhétorique

Ce script prend en entrée un fichier JSON contenant l'analyse structurée
et génère un rapport formaté (XLSX, JSON, ou Markdown).

Usage:
    python generate_analysis.py <input.json> <output_file> [--format <format>]

Exemple:
  python generate_analysis.py analysis.json rapport_analyse.xlsx
  python generate_analysis.py analysis.json analysis.json --format json
  python generate_analysis.py analysis.json rapport.md --format md
"""

import argparse
import json
import sys
from pathlib import Path

import scripts.formatters.excel as excel
import scripts.formatters.json as json_formatter
import scripts.formatters.markdown as markdown


def main():
    parser = argparse.ArgumentParser(
        description="Génère un rapport d'analyse rhétorique à partir d'un fichier JSON.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Chemin vers le fichier JSON d'entrée contenant l'analyse structurée."
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Chemin vers le fichier de sortie du rapport."
    )
    parser.add_argument(
        "--format",
        choices=["xlsx", "json", "md"],
        default="xlsx",
        help="Format du fichier de sortie (par défaut: xlsx)."
    )

    args = parser.parse_args()

    # Charger les données d'analyse
    try:
        with open(args.input_file, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier non trouvé: {args.input_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Erreur: Le fichier JSON d'entrée est invalide: {args.input_file}")
        sys.exit(1)

    # Dispatcher vers le bon formateur
    if args.format == "xlsx":
        success = excel.save_report(data, args.output_file)
    elif args.format == "json":
        success = json_formatter.save_report(data, args.output_file)
    elif args.format == "md":
        success = markdown.save_report(data, args.output_file)
    else:
        print(f"❌ Erreur: Format de sortie '{args.format}' non supporté.")
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
