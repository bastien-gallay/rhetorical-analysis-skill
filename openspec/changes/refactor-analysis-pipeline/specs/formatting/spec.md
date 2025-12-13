## ADDED Requirements

### Requirement: Formater la sortie en XLSX

Le système **MUST** pouvoir générer un rapport d'analyse au format XLSX.

#### Scenario: Génération du rapport XLSX
- **GIVEN** des données d'analyse valides et un chemin de fichier de sortie.
- **WHEN** l'utilisateur demande une sortie au format `xlsx`.
- **THEN** le système doit générer un fichier `.xlsx` au chemin spécifié, contenant les onglets "Analyse rhétorique", "Détail Toulmin", "Évaluation sources (CRAAP)", "Synthèse" et "Légende", formatés de manière identique au comportement actuel.

### Requirement: Formater la sortie en JSON

Le système **MUST** pouvoir générer un rapport d'analyse au format JSON.

#### Scenario: Génération du rapport JSON
- **GIVEN** des données d'analyse valides et un chemin de fichier de sortie.
- **WHEN** l'utilisateur demande une sortie au format `json`.
- **THEN** le système doit générer un fichier `.json` au chemin spécifié, contenant les données d'analyse originales, formatées avec une indentation de 4 espaces pour la lisibilité.

### Requirement: Formater la sortie en Markdown

Le système **MUST** pouvoir générer un rapport d'analyse au format Markdown.

#### Scenario: Génération du rapport Markdown
- **GIVEN** des données d'analyse valides et un chemin de fichier de sortie.
- **WHEN** l'utilisateur demande une sortie au format `md`.
- **THEN** le système doit générer un fichier `.md` au chemin spécifié.
- **AND** le fichier Markdown doit contenir :
    - Les métadonnées de l'analyse.
    - Une section de synthèse avec les points forts, faibles et les motifs récurrents.
    - Une section par argument analysé, présentée sous forme de tableau ou de liste, incluant la thèse, le type de raisonnement, les sophismes, la fiabilité et l'évaluation.
    - Une section détaillant le modèle de Toulmin pour chaque argument.
    - Une section pour l'évaluation CRAAP des sources.

## MODIFIED Requirements

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
