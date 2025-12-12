# CLAUDE.md - Instructions pour Claude Code

## Contexte du projet

Ce projet est un **skill Claude** pour l'analyse rhétorique et épistémologique d'articles.
Il combine le modèle de Toulmin, le test CRAAP, et un catalogue de sophismes.

<!-- OPENSPEC:START -->
## OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## Structure

- `SKILL.md` : Point d'entrée du skill (lu par Claude quand le skill est activé)
- `scripts/` : Scripts Python exécutables
- `references/` : Documentation de référence (frameworks, catalogue de sophismes)
- `assets/` : Fichiers d'exemple et templates
- `tests/` : Tests unitaires et fixtures

## Commandes fréquentes

```bash
# Installer les dépendances
uv sync --all-extras

# Lancer les tests
uv run pytest tests/ -v

# Générer un rapport depuis un JSON
uv run python scripts/generate_analysis.py input.json output.xlsx

# Valider le skill avant packaging
uv run python scripts/validate_skill.py .

# Packager le skill
zip -r rhetorical-analysis-skill.skill . -x "*.git*" -x "*__pycache__*" -x "*.pytest_cache*" -x "tests/*"
```

## Conventions

- **Python** : Python 3.10+, type hints, docstrings Google style
- **Nommage** : snake_case pour les fichiers Python, kebab-case pour le skill
- **JSON** : Schéma d'analyse dans `assets/example_analysis.json`

## Objectifs de développement

### Phase 1 : Consolidation (actuel)
- [x] Script de génération XLSX
- [x] Catalogue de sophismes
- [x] Documentation des frameworks
- [ ] Tests unitaires pour generate_analysis.py
- [ ] Validation du schéma JSON (jsonschema)

### Phase 2 : Automatisation
- [ ] Script `analyze_url.py` : fetch URL + extraction texte + structure HTML
- [ ] Intégration avec web_fetch pour analyse directe
- [ ] Mode batch pour analyser plusieurs articles

### Phase 3 : Visualisation
- [ ] Export Mermaid pour graphe d'argumentation
- [ ] Export HTML interactif
- [ ] Dashboard de comparaison multi-articles

### Phase 4 : Intégration LLM
- [ ] Prompt template optimisé pour l'analyse
- [ ] Validation automatique de la cohérence des scores
- [ ] Détection automatique du type de texte (militant, académique, journalistique)

## Notes pour Claude

- Le skill doit rester **léger** (< 500 lignes dans SKILL.md)
- Privilégier les **références externes** pour le détail
- Le JSON d'analyse est le **contrat d'interface** entre Claude et le script
- Toujours **tester** les modifications du script avant de commiter

## Ressources

- [Modèle de Toulmin](https://en.wikipedia.org/wiki/Toulmin_model)
- [Test CRAAP](https://en.wikipedia.org/wiki/CRAAP_test)
- [ArgMining Workshop](https://argmining-org.github.io/)
- [Skill Creator Guide](/mnt/skills/examples/skill-creator/SKILL.md)
