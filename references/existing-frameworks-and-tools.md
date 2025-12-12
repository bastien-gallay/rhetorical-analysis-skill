# Frameworks méthodologiques et outils d'analyse argumentative

## Frameworks académiques établis

### 1. Modèle de Toulmin (1958)
**Origine** : Stephen Toulmin, "The Uses of Argument"
**Usage** : Standard académique pour l'analyse argumentative

| Composant | Description |
|-----------|-------------|
| Claim | La thèse défendue |
| Grounds | Les preuves/données |
| Warrant | Le lien logique (souvent implicite) |
| Backing | Support additionnel du warrant |
| Qualifier | Nuances ("probablement", "en général") |
| Rebuttal | Contre-arguments reconnus |

**Forces** : Structure claire, applicable à tout type de texte
**Limites** : Peut être trop rigide pour les discours complexes

### 2. Test CRAAP (2004)
**Origine** : Sarah Blakeslee, CSU Chico
**Usage** : Évaluation de la fiabilité des sources

| Critère | Questions clés |
|---------|----------------|
| Currency | L'info est-elle à jour ? |
| Relevance | Pertinente pour le sujet ? |
| Authority | L'auteur est-il crédible ? |
| Accuracy | Les faits sont-ils vérifiables ? |
| Purpose | Quelle est l'intention ? |

### 3. Méthode SIFT (2019)
**Origine** : Mike Caulfield
**Usage** : Évaluation rapide d'information en ligne

- **Stop** : Ne pas réagir immédiatement
- **Investigate** : Vérifier la source
- **Find** : Chercher une meilleure couverture
- **Trace** : Remonter à la source originale

### 4. Pragma-dialectique (van Eemeren)
**Usage** : Analyse des discussions argumentatives comme actes de langage
**Principe** : L'argumentation est un processus de résolution de différends

---

## Domaine de recherche : Argument Mining (NLP)

**Définition** : Extraction automatique de structures argumentatives par traitement du langage naturel

**Conférences principales** :
- ArgMining Workshop (annuel, co-localisé avec ACL/EMNLP)
- COMMA (Computational Models of Argument)

**Tâches types** :
- Segmentation des composants argumentatifs
- Classification (claim, premise, evidence)
- Détection des relations (support, attack)
- Évaluation de la qualité argumentative

**Projets notables** :
- IBM Project Debater (discontinued mais influent)
- Argument Search Engine (args.me)

**Datasets annotés** :
- Persuasive Essays Corpus (TU Darmstadt)
- US Presidential Debates Corpus
- FEVER (fact verification)

---

## Outils existants (grand public)

### Détecteurs de sophismes basés sur LLM

| Outil | Type | Accès |
|-------|------|-------|
| Fallacy Finder (Word.Studio) | Web app | Gratuit |
| logicalfallacies.org/detector | Web app | Gratuit (limité) |
| Fallacy Finder GPT | ChatGPT Plus | Payant |
| Fallacy Checker GPT | ChatGPT Plus | Payant |
| Discourse Analyzer AI | Web app | Freemium |

### Outils open source

| Projet | Lien | Description |
|--------|------|-------------|
| tmakesense/logical-fallacy | GitHub | Dataset + détecteur ML |
| namiyousef/argument-mining | GitHub | Pipeline NLP complet |
| causalNLP/logical-fallacy | GitHub | Dataset annoté original |

### Plateformes académiques

- **args.me** : Moteur de recherche d'arguments
- **Kialo** : Plateforme de débat structuré
- **ProCon.org** : Arguments pour/contre sur sujets d'actualité

---

## Comparaison avec l'analyse que j'ai produite

| Dimension | Mon analyse | Ce que les outils existants font |
|-----------|-------------|----------------------------------|
| Granularité | Argument par argument | Souvent au niveau phrase/paragraphe |
| Évaluation sources | Intégrée (CRAAP adapté) | Rarement intégrée |
| Contexte militant | Reconnu explicitement | Généralement ignoré |
| Format sortie | Tableau structuré réutilisable | Texte narratif |
| Nuance | Échelle 1-5 avec justification | Binaire (sophisme/pas sophisme) |

---

## Enrichissements possibles pour le skill

### 1. Intégration de vérification factuelle
- Croiser avec des bases de fact-checking (ClaimBuster, Google Fact Check)
- Web search automatique des sources citées

### 2. Analyse de sentiment/tonalité
- Détecter les appels émotionnels (pathos vs logos)
- Mesurer l'intensité du langage

### 3. Cartographie des acteurs
- Identifier les parties prenantes mentionnées
- Mapper leurs intérêts potentiels

### 4. Analyse comparative
- Comparer avec d'autres textes sur le même sujet
- Identifier les arguments manquants (blind spots)

### 5. Visualisation
- Graphe d'argumentation (claims → evidence → rebuttals)
- Timeline des sources citées

---

## Limites inhérentes à l'analyse automatisée

1. **Contexte culturel** : Les normes argumentatives varient selon les cultures
2. **Ironie/second degré** : Difficile à détecter automatiquement
3. **Expertise domaine** : Impossible de vérifier certaines affirmations sans spécialiste
4. **Biais de l'analyste** : Même un LLM a des biais dans son training
5. **Textes complexes** : Arguments imbriqués, ironie, métaphores filées

**Recommandation** : L'analyse automatisée est un outil d'aide, pas un juge final. Toujours croiser avec un regard humain critique.
