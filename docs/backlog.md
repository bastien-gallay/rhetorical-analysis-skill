# Backlog

## Priorité haute

- ~~**CI/CD** : GitHub Actions pour les tests et le packaging~~ ✅
- **Fallbacks lorsque le lien est inaccessible** : Gérer les erreurs HTTP, les pages vides, les blockages en proposant à l'utilisateur de fournir le contenu directement (Copier-coller ou imprimer ver PDF)

## Priorité moyenne

- **Intégration des évaluations** : Intégrer la méthodologie de benchmark pour valider les performances du skill avec `scripts/evaluate.py` et `docs/benchmark-protocol.md`
- **Export Mermaid** : Visualisation du graphe d'argumentation

## Priorité basse

- **Prompt template** : Optimiser le prompt pour améliorer la qualité des analyses
- **Mode batch** : Analyser plusieurs articles en une passe
- **Validation JSON** : Implémenter un schéma jsonschema pour valider les analyses
- **Extraction enrichie** : Extraire métadonnées (auteur, date de publication, images) lors du fetch d'URL pour contextualiser l'analyse

## Idées à explorer

- Mode interactif où Claude pose des questions de clarification
- Versionner les analyses pour suivre l'évolution d'un débat dans le temps
