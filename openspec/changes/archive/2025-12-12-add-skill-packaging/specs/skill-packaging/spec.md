# Skill Packaging

Capacité de packaging automatisé du skill pour distribution.

## ADDED Requirements

### Requirement: Skill Validation

Le système SHALL valider le skill avant packaging en vérifiant le SKILL.md.

#### Scenario: SKILL.md valide

- **WHEN** le fichier SKILL.md existe avec un frontmatter YAML valide (name, description)
- **AND** le fichier fait moins de 500 lignes
- **THEN** la validation réussit

#### Scenario: SKILL.md manquant

- **WHEN** le fichier SKILL.md n'existe pas
- **THEN** la validation échoue avec un message d'erreur explicite

#### Scenario: SKILL.md trop long

- **WHEN** le fichier SKILL.md dépasse 500 lignes
- **THEN** la validation échoue avec le nombre de lignes actuel

### Requirement: Archive Generation

Le système SHALL générer une archive ZIP distribuable contenant les fichiers du skill.

#### Scenario: Génération réussie

- **WHEN** la validation du skill réussit
- **THEN** une archive `.skill` est créée contenant uniquement les fichiers nécessaires
- **AND** le nom de l'archive inclut la version (ex: `rhetorical-analysis-0.1.0.skill`)

#### Scenario: Fichiers exclus par défaut

- **WHEN** l'archive est générée
- **THEN** les patterns suivants sont exclus : `.git/`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `tests/`, `*.egg-info/`, `.claude/`

### Requirement: Dry Run Mode

Le système SHALL permettre de prévisualiser le contenu du package sans le créer.

#### Scenario: Mode dry-run

- **WHEN** l'utilisateur exécute le script avec `--dry-run`
- **THEN** la liste des fichiers qui seraient inclus est affichée
- **AND** aucune archive n'est créée

### Requirement: Version Management

Le système SHALL extraire la version depuis pyproject.toml pour nommer l'archive.

#### Scenario: Version présente

- **WHEN** pyproject.toml contient une clé `version` dans `[project]`
- **THEN** cette version est utilisée dans le nom de l'archive

#### Scenario: Version absente

- **WHEN** pyproject.toml ne contient pas de version
- **THEN** le suffixe `dev` est utilisé (ex: `rhetorical-analysis-dev.skill`)
