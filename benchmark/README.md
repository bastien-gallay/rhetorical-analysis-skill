# Benchmark d'analyse rhétorique

Ce répertoire contient les ressources pour évaluer et améliorer le skill d'analyse rhétorique.

## Structure

```
benchmark/
├── articles/                    # Articles sources (texte brut ou HTML)
│   └── french/
│       ├── militant/           # Articles militants, tribunes
│       ├── journalistique/     # Articles de presse
│       └── academique/         # Articles scientifiques
├── annotations/
│   ├── gold/                   # Annotations de référence (humain)
│   └── model/                  # Annotations générées par Claude
├── external/                   # Datasets externes (FixedLogic, etc.)
└── results/                    # Résultats d'évaluation
```

## Fichiers gold standard

| ID  | Article        | Type     | Langue | Annotateur | Date       |
| --- | -------------- | -------- | ------ | ---------- | ---------- |
| 001 | Atécopol - IAg | militant | FR     | expert     | 2025-12-12 |

## Usage

### Évaluer une analyse

```bash
# Fichier unique
python scripts/evaluate.py benchmark/annotations/gold/001.json benchmark/annotations/model/001.json

# Lot complet
python scripts/evaluate.py --batch benchmark/annotations/gold/ benchmark/annotations/model/ -o results/eval.csv
```

### Ajouter une annotation gold

1. Copier le template depuis `assets/example_analysis.json`
2. Remplir tous les champs pour chaque argument
3. Placer dans `annotations/gold/` avec le format `NNN_nom_article.json`
4. Documenter dans ce README

## Format d'annotation

Voir `assets/example_analysis.json` pour le schéma complet.

Champs obligatoires par argument :
- `id` : Numéro séquentiel
- `label` : Résumé court
- `claim` : Thèse défendue
- `fallacies` : Liste des sophismes détectés (vide si aucun)
- `reliability` : Score 1-5

## Datasets externes à intégrer

- [ ] FixedLogic (sophismes) : <https://github.com/tmakesense/logical-fallacy>
- [ ] AAEC subset (structure Toulmin) : à extraire
- [ ] PTC Corpus (propagande) : pour tests avancés

## Métriques cibles

| Métrique        | Baseline actuelle | Cible v1.0 | Cible v2.0 |
| --------------- | ----------------- | ---------- | ---------- |
| Fallacy F1      | TBD               | > 0.50     | > 0.70     |
| Reliability MAE | TBD               | < 1.0      | < 0.5      |
