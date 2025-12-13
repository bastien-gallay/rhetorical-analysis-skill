# Datasets de référence et protocole d'amélioration

## 1. Datasets disponibles pour la validation

### A. Structure argumentative (Toulmin / Claim-Premise)

| Dataset | Taille | Annotations | Langue | Source |
|---------|--------|-------------|--------|--------|
| **Argument Annotated Essays Corpus (AAEC)** | 402 essays, 6089 composants | Major Claim, Claim, Premise, Support/Attack relations | EN | [TU Darmstadt](https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/2422) |
| **AAEC Extended** (Carlile et al.) | 102 essays subset | + Persuasiveness score, Ethos/Pathos/Logos, Evidence quality | EN | Même source |
| **US Presidential Debates** | 39 débats, 29k composants | Claims, Premises | EN | [Papers with Code](https://paperswithcode.com/dataset/us-presidential-debates) |
| **Microtexts Corpus** | 112 textes courts | Argumentation complète | EN/DE | Peldszus & Stede |
| **AbstRCT** (Medical) | 700 abstracts | Claims, Premises (domaine médical) | EN | [GitHub](https://github.com/Ukraine-NLP/abstRCT) |

**Dataset principal recommandé** : AAEC de Stab & Gurevych (2017) — le standard de facto en Argument Mining.

### B. Détection de sophismes (Logical Fallacies)

| Dataset | Taille | Types de sophismes | Langue | Source |
|---------|--------|-------------------|--------|--------|
| **LOGIC** | 2453 exemples (2226 après nettoyage) | 13 types | EN | [causalNLP/logical-fallacy](https://github.com/causalNLP/logical-fallacy) |
| **LogicClimate** | Challenge set | Idem, domaine climat | EN | Même repo |
| **FixedLogic** | 2226 exemples (nettoyé) | 13 types | EN | [tmakesense/logical-fallacy](https://github.com/tmakesense/logical-fallacy/tree/main/dataset-fixed) |
| **MAFALDA** | 7706 commentaires | Multiple types | EN | [arxiv 2410.03457](https://arxiv.org/abs/2410.03457) |
| **PTC Corpus** (Propaganda) | 451 articles, 20k phrases | 18 techniques (12 = fallacies) | EN | SemEval-2020 Task 11 |
| **FALCON** | Tweets COVID | 6 types de fallacies | EN | Musi et al. 2022 |

**Dataset principal recommandé** : FixedLogic (version nettoyée du dataset causalNLP).

### C. Évaluation de la qualité argumentative

| Dataset | Description | Métriques |
|---------|-------------|-----------|
| **AAEC + Persuasiveness** | Extension du AAEC | Score persuasion, Eloquence, Specificity, Relevance, Evidence |
| **IBM Debater datasets** | Arguments Wikipedia | Claim detection, Evidence quality |
| **args.me** | Moteur de recherche d'arguments | Arguments pro/con annotés |

---

## 2. Types de sophismes couverts par les datasets

Les 13 types du dataset LOGIC (alignés avec notre catalogue) :

1. **Ad Hominem** - Attaque la personne
2. **Ad Populum** - Appel à la popularité
3. **Appeal to Emotion** - Appel à l'émotion
4. **Circular Reasoning** - Raisonnement circulaire
5. **Equivocation** - Équivoque/Ambiguïté
6. **Fallacy of Credibility** - Appel à l'autorité invalide
7. **Fallacy of Extension** - Homme de paille (Strawman)
8. **Fallacy of Logic** - Erreur logique formelle
9. **Fallacy of Relevance** - Non sequitur
10. **False Causality** - Fausse cause
11. **False Dilemma** - Faux dilemme
12. **Faulty Generalization** - Généralisation hâtive
13. **Intentional** - Manipulation intentionnelle

---

## 3. Protocole d'amélioration du skill

### Phase 1 : Création d'un gold standard local (semaine 1-2)

**Objectif** : Avoir 20-30 exemples annotés manuellement pour calibrer.

```
benchmark/
├── articles/
│   ├── 001_atecopol_iag.json      # L'article analysé aujourd'hui
│   ├── 002_tribune_climat.json
│   └── ...
├── annotations/
│   ├── 001_human_expert.json      # Annotation humaine de référence
│   ├── 001_claude_v1.json         # Output de Claude v1
│   └── 001_claude_v2.json         # Output après amélioration
└── scores/
    └── comparison_matrix.csv       # Métriques de comparaison
```

**Actions** :
1. Sélectionner 10 articles variés (militants, journalistiques, académiques)
2. Les annoter manuellement selon le schéma du skill
3. Faire analyser par Claude
4. Comparer et mesurer l'écart

### Phase 2 : Métriques d'évaluation (semaine 2-3)

**Métriques proposées** :

| Dimension | Métrique | Calcul |
|-----------|----------|--------|
| **Segmentation** | IoU (Intersection over Union) | Overlap entre segments identifiés |
| **Classification Toulmin** | F1 par composant | Claim/Grounds/Warrant |
| **Détection sophismes** | Precision/Recall/F1 | Par type de sophisme |
| **Score fiabilité** | MAE (Mean Absolute Error) | |expert - model| |
| **Accord inter-annotateur** | Cohen's Kappa | Si plusieurs annotateurs |

**Script d'évaluation** :
```python
def evaluate_analysis(gold: dict, predicted: dict) -> dict:
    """Compare une annotation de référence avec la sortie du modèle."""
    return {
        "segmentation_iou": compute_iou(gold["arguments"], predicted["arguments"]),
        "toulmin_f1": compute_toulmin_f1(gold, predicted),
        "fallacy_f1": compute_fallacy_f1(gold, predicted),
        "reliability_mae": compute_reliability_mae(gold, predicted),
    }
```

### Phase 3 : Calibration itérative (semaine 3-4)

**Workflow** :

```
┌─────────────────┐
│  Article test   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Analyse Claude  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Comparaison    │◄──── Gold standard
│  avec référence │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Identification  │
│ des erreurs     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Mise à jour du  │
│ SKILL.md        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Re-test sur     │
│ benchmark       │
└─────────────────┘
```

**Types d'erreurs à traquer** :
- Faux positifs (sophismes détectés à tort)
- Faux négatifs (sophismes manqués)
- Erreurs de classification (strawman classé comme ad hominem)
- Scores de fiabilité trop généreux ou trop sévères
- Structure Toulmin mal identifiée

### Phase 4 : Enrichissement avec datasets externes (semaine 4+)

**Intégration progressive** :

1. **Importer FixedLogic** comme référence pour les sophismes
   ```bash
   git clone https://github.com/tmakesense/logical-fallacy
   cp dataset-fixed/*.csv benchmark/external/
   ```

2. **Extraire des exemples du AAEC** pour calibrer la structure Toulmin

3. **Créer des tests automatisés** :
   ```python
   @pytest.mark.parametrize("example", load_fixedlogic_samples())
   def test_fallacy_detection(example):
       result = analyze_text(example["text"])
       assert example["fallacy_type"] in result["detected_fallacies"]
   ```

---

## 4. Structure proposée pour le benchmark

```
benchmark/
├── README.md                    # Description du protocole
├── config.yaml                  # Configuration (seuils, types de sophismes)
├── articles/
│   ├── french/                  # Articles en français
│   │   ├── militant/
│   │   ├── journalistique/
│   │   └── academique/
│   └── english/                 # Pour comparaison avec datasets standards
├── annotations/
│   ├── gold/                    # Annotations humaines de référence
│   └── model/                   # Outputs du modèle
├── external/
│   ├── fixedlogic/             # Dataset de sophismes
│   └── aaec_subset/            # Échantillon du AAEC
├── scripts/
│   ├── evaluate.py             # Calcul des métriques
│   ├── compare.py              # Comparaison gold vs model
│   └── report.py               # Génération de rapports
└── results/
    ├── metrics_history.csv     # Évolution des scores dans le temps
    └── error_analysis/         # Analyses d'erreurs détaillées
```

---

## 5. Checklist de démarrage

- [ ] Télécharger FixedLogic : `git clone https://github.com/tmakesense/logical-fallacy`
- [ ] Annoter manuellement 5 articles français variés
- [ ] Créer le script `evaluate.py` avec les métriques de base
- [ ] Établir une baseline avec la version actuelle du skill
- [ ] Documenter les premiers écarts identifiés
- [ ] Itérer sur le SKILL.md et le catalogue de sophismes

---

## 6. Ressources complémentaires

### Papiers de référence
- Stab & Gurevych (2017) - "Parsing Argumentation Structures in Persuasive Essays"
- Jin et al. (2022) - "Logical Fallacy Detection" (Findings of EMNLP)
- Da San Martino et al. (2019) - "Fine-grained Analysis of Propaganda in News Articles"

### Outils
- [args.me](https://args.me/) - Moteur de recherche d'arguments
- [Kialo](https://www.kialo.com/) - Plateforme de débat structuré (exemples annotés)
- [ProCon.org](https://www.procon.org/) - Arguments pro/con structurés

### Communauté
- [ArgMining Workshop](https://argmining-org.github.io/) - Workshop annuel
- [Computational Argumentation](https://www.arg.tech/) - Groupe de recherche
