# Proposal: add-github-packaging-workflow

## Context

Le projet dispose d'un script `scripts/package_skill.py` permettant de créer une archive `.skill` distribuable. Ce script valide le SKILL.md et génère un fichier ZIP avec les fichiers nécessaires, en excluant les fichiers de développement.

Actuellement, le packaging doit être effectué manuellement en local. Pour faciliter la distribution et garantir la reproductibilité, il est nécessaire d'automatiser ce processus via GitHub Actions.

## Problem Statement

- **Processus manuel** : Le packaging nécessite d'exécuter manuellement le script `package_skill.py`
- **Manque de reproductibilité** : Pas de garantie que l'environnement de packaging est identique entre développeurs
- **Distribution manuelle** : Les archives `.skill` ne sont pas automatiquement disponibles pour les utilisateurs
- **Absence de CI** : Pas de validation automatique que le skill est packageable avant merge

## Proposed Solution

Créer un GitHub Action qui :

1. **Trigger sur tags** : Se déclenche lors de la création d'un tag de version (ex: `v0.1.0`)
2. **Validation** : Utilise le script existant `package_skill.py` pour valider le skill
3. **Packaging** : Génère l'archive `.skill` avec la version extraite du tag
4. **Contrôle d'intégrité** : Calcule les checksums SHA256 de l'archive pour vérification
5. **Publication** : Crée une GitHub Release avec l'archive et les checksums en artifacts téléchargeables
6. **Documentation** : Met à jour le README avec les instructions de téléchargement et d'installation

### Workflow attendu

```
Developer pushes tag v0.1.0
    ↓
GitHub Action triggered
    ↓
Setup Python + uv
    ↓
Run package_skill.py
    ↓
Generate SHA256 checksums
    ↓
Create GitHub Release v0.1.0
    ↓
Upload .skill artifact + checksums to release
```

### Contrôle d'intégrité

Pour chaque release, le workflow génère :
- **SHA256 checksum** : Hash de l'archive `.skill` pour vérification d'intégrité
- **Fichier checksums.txt** : Contient le hash et le nom du fichier au format standard

Les utilisateurs peuvent vérifier l'intégrité après téléchargement :
```bash
# Linux/macOS
sha256sum -c checksums.txt

# Windows PowerShell
Get-FileHash rhetorical-analysis-0.1.0.skill -Algorithm SHA256
```

### Documentation utilisateur

Le README sera mis à jour avec :
- **Section Installation** : Lien vers les releases et instructions de téléchargement
- **Vérification d'intégrité** : Commandes pour valider les checksums
- **Badge release** : Badge GitHub affichant la dernière version disponible

## Alternatives Considered

1. **Trigger sur push main** : Rejeté car crée trop de releases intermédiaires
2. **Utiliser GitHub Packages** : Rejeté car .skill n'est pas un format standard package
3. **Build artifact seulement** : Rejeté car nécessite accès aux artifacts GitHub (expires)

## Impact

- **Users** : 
  - Peuvent télécharger les releases directement depuis GitHub
  - Peuvent vérifier l'intégrité des packages téléchargés
  - Ont des instructions claires d'installation dans le README
- **Development** : 
  - Workflow de release standardisé et reproductible
  - Checksums générés automatiquement pour chaque release
- **CI/CD** : Base pour ajouter tests et validations supplémentaires
- **Documentation** : README maintenu à jour automatiquement avec les liens de téléchargement

## Risks

- **Tag/version mismatch** : Si le tag Git ne correspond pas à la version dans `pyproject.toml`
  - **Mitigation** : Le nom de l'archive inclut la version du pyproject, le mismatch sera visible
- **Script failure en CI** : Si `package_skill.py` échoue en CI mais pas en local
  - **Mitigation** : Utiliser exactement le même runtime (Python + uv) que le développement

## Dependencies

- Nécessite que `scripts/package_skill.py` soit fonctionnel (déjà le cas)
- Pas de dépendance sur d'autres changes en cours

## Success Criteria

- [x] Workflow GitHub Actions créé et fonctionnel
- [x] Trigger sur création de tag Git
- [x] Archive .skill générée avec succès
- [x] Checksums SHA256 générés pour l'archive
- [x] GitHub Release créée automatiquement avec artifacts téléchargeables (.skill + checksums)
- [x] README mis à jour avec section Installation/Download
- [x] Instructions de vérification d'intégrité documentées
- [x] Badge de release ajouté au README
- [x] Documentation du workflow de release pour les mainteneurs

## Related Specs

- **ci-skill-packaging** (new): Spécification du workflow CI pour le packaging automatique
- **skill-packaging** (existing): Spécification du script de packaging déjà implémenté
