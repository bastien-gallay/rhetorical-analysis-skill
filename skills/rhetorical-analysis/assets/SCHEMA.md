# Format d'analyse rhétorique - Schéma JSON

Ce document décrit le format JSON utilisé pour les analyses rhétoriques produites par
le skill.

## Structure générale

```json
{
    "metadata": { ... },
    "arguments": [ ... ],
    "synthesis": { ... }
}
```

## Metadata

Informations sur l'article analysé et l'analyse elle-même.

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `title` | string | Oui | Titre de l'article analysé |
| `source` | string | Oui | URL ou référence de la source |
| `date_publication` | string | Non | Date de publication (YYYY-MM-DD) |
| `date_analysis` | string | Oui | Date de l'analyse (YYYY-MM-DD) |
| `analyst` | string | Non | Auteur de l'analyse |
| `license` | string | Non | Licence du contenu source |
| `note` | string | Non | Remarques sur l'analyse |

## Arguments

Liste des arguments identifiés dans le texte. Chaque argument suit le modèle de Toulmin.

### Structure d'un argument

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `id` | integer | Oui | Identifiant unique de l'argument |
| `label` | string | Oui | Titre court décrivant l'argument |
| `original_text` | string | Oui | Extrait du texte source |
| `claim` | string | Oui | Affirmation/thèse de l'argument |
| `grounds` | string | Oui | Preuves/données supportant la thèse |
| `warrant` | string | Oui | Justification liant les preuves à la thèse |
| `backing` | string | Non | Fondement de la justification |
| `qualifier` | string | Non | Nuances/conditions de validité |
| `rebuttal` | string | Non | Contre-arguments reconnus |
| `reasoning_type` | string | Non | Type de raisonnement utilisé |
| `fallacies` | array | Non | Sophismes identifiés |
| `reliability` | integer | Oui | Score de fiabilité (1-5) |
| `reliability_rationale` | string | Oui | Justification du score |
| `sources_cited` | array | Non | Sources citées dans l'argument |
| `comment` | string | Non | Commentaire de l'analyste |

### Score de fiabilité

| Score | Signification |
|-------|---------------|
| 1 | Très faible - Argument fallacieux ou non sourcé |
| 2 | Faible - Sources douteuses ou raisonnement fragile |
| 3 | Moyen - Quelques faiblesses mais globalement acceptable |
| 4 | Bon - Bien sourcé avec raisonnement valide |
| 5 | Excellent - Sources de référence, raisonnement rigoureux |

### Sophismes (fallacies)

```json
{
    "name": "Nom du sophisme",
    "description": "Explication de pourquoi c'est un sophisme ici",
    "severity": "légère | modérée | grave"
}
```

Voir [fallacies-catalog.md](../references/fallacies-catalog.md) pour la liste
des sophismes courants.

### Sources citées

Chaque source inclut un score CRAAP :

```json
{
    "name": "Nom de la source",
    "craap_score": {
        "currency": 1-5,
        "relevance": 1-5,
        "authority": 1-5,
        "accuracy": 1-5,
        "purpose": 1-5
    }
}
```

## Synthesis

Résumé de l'analyse globale.

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `strengths` | array[string] | Oui | Points forts de l'argumentation |
| `weaknesses` | array[string] | Oui | Faiblesses identifiées |
| `recurring_patterns` | array[string] | Non | Motifs argumentatifs récurrents |
| `overall_craap_score` | object | Non | Score CRAAP global de l'article |
| `methodological_note` | string | Non | Note méthodologique |

## Exemples

Deux exemples sont fournis dans ce répertoire :

- `example_analysis.json` : Exemple synthétique (contenu fictif, CC0)
- `example_ddhc_1789.json` : Analyse de la DDHC 1789 (domaine public)

## Créer vos propres analyses

Pour analyser vos propres articles :

1. Copiez la structure d'un exemple existant
2. Remplacez les métadonnées par celles de votre source
3. Identifiez les arguments principaux du texte
4. Pour chaque argument, remplissez les champs du modèle de Toulmin
5. Évaluez la fiabilité et identifiez les sophismes éventuels
6. Rédigez la synthèse

Le script `generate_analysis.py` peut ensuite générer des rapports XLSX, JSON ou
Markdown à partir de votre fichier d'analyse.
