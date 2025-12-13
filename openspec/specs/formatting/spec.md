# formatting Specification

## Purpose
TBD - created by archiving change refactor-analysis-pipeline. Update Purpose after archive.
## Requirements
### Requirement: Sélectionner le format de sortie via le CLI

Le script principal **MUST** permettre à l'utilisateur de choisir le format de sortie via une option en ligne de commande.

#### Scenario: Format par défaut (XLSX)
- **GIVEN** un fichier d'entrée et un fichier de sortie, sans spécifier de format.
- **WHEN** le script `generate_analysis.py` est exécuté.
- **THEN** le système doit générer un rapport au format `xlsx` par défaut.

#### Scenario: Sélection explicite d'un format
- **GIVEN** un fichier d'entrée, un fichier de sortie et un format de sortie valide (`xlsx`, `json`, ou `md`).
- **WHEN** le script `generate_analysis.py` est exécuté avec l'option `--format <format>`.
- **THEN** le système doit générer un rapport dans le format spécifié.

#### Scenario: Format invalide
- **GIVEN** un format de sortie non valide (ex: `pdf`).
- **WHEN** le script `generate_analysis.py` est exécuté.
- **THEN** le système doit afficher un message d'erreur listant les formats valides et se terminer.

