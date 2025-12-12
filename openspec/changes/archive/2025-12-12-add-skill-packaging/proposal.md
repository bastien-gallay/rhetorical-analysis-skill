# Change: Packaging automatisé du Skill

## Why

La commande de packaging actuelle est manuelle (`zip -r ...`) et ne garantit pas la validation du skill avant distribution. Un script dédié permettrait d'automatiser la validation et le packaging en une seule commande.

## What Changes

- Ajout d'un script `scripts/package_skill.py` pour automatiser le packaging
- Validation automatique du SKILL.md (frontmatter, taille < 500 lignes)
- Génération d'un fichier `.skill` (archive ZIP) prêt à distribuer
- Exclusion automatique des fichiers non nécessaires (.git, .venv, tests, cache)
- Gestion de la version basée sur `pyproject.toml`

## Impact

- Affected specs: Nouveau spec `skill-packaging`
- Affected code: `scripts/package_skill.py` (nouveau)
