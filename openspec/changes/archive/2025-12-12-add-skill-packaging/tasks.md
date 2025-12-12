# Tasks: add-skill-packaging

## 1. Implementation

- [x] 1.1 Créer le script `scripts/package_skill.py` avec CLI argparse
- [x] 1.2 Implémenter la validation du SKILL.md (frontmatter YAML, limite de lignes)
- [x] 1.3 Implémenter la génération de l'archive ZIP avec exclusions configurables
- [x] 1.4 Extraire la version depuis pyproject.toml pour nommer l'archive
- [x] 1.5 Ajouter option `--dry-run` pour prévisualiser le contenu du package

## 2. Tests

- [x] 2.1 Tests unitaires pour la validation du SKILL.md
- [x] 2.2 Tests unitaires pour la génération de l'archive
- [x] 2.3 Test d'intégration du workflow complet

## 3. Documentation

- [x] 3.1 Mettre à jour CLAUDE.md avec la nouvelle commande
- [x] 3.2 Documenter les patterns d'exclusion dans le script
