# Proposition : Séparer l'extraction et le formatage de la sortie

## Problème

Actuellement, le script `generate_analysis.py` est monolithique. Il lit une analyse rhétorique au format JSON et génère **uniquement** un fichier XLSX. Cette conception rigide empêche d'étendre facilement le skill pour produire d'autres types de rapports (par exemple, Markdown ou JSON brut), qui peuvent être plus adaptés à d'autres usages (intégration avec d'autres outils, relecture rapide, etc.).

Le script couple la logique de lecture des données avec la logique de mise en forme spécifique à Excel (`openpyxl`), ce qui le rend difficile à maintenir et à faire évoluer.

## Solution proposée

Nous proposons de refactoriser le pipeline d'analyse en deux étapes distinctes et modulaires :

1. **Chargement des données** : Un module central sera responsable de la lecture et de la validation du fichier JSON d'entrée. Cette étape produira une structure de données Python (un dictionnaire) qui servira de "source de vérité" pour l'étape suivante.
2. **Formatage de la sortie** : Des modules de formatage distincts ("formatters") seront créés, chacun spécialisé dans la génération d'un type de fichier de sortie spécifique.

Au départ, nous implémenterons trois formats :

- **Excel (`xlsx`)** : Le comportement actuel, encapsulé dans son propre module.
- **JSON (`json`)** : Une sortie JSON brute et formatée ("pretty-printed"), utile pour le débogage ou l'intégration avec d'autres outils.
- **Markdown (`md`)** : Un rapport textuel lisible, facile à partager et à versionner.

Le script principal `generate_analysis.py` sera modifié pour accepter un argument `--format` qui permettra à l'utilisateur de choisir le format de sortie désiré. Le format par défaut restera `xlsx` pour assurer la rétrocompatibilité.

## Avantages

- **Extensibilité** : L'ajout de nouveaux formats (HTML, PDF, etc.) deviendra trivial, il suffira de créer un nouveau module de formatage.
- **Maintenabilité** : La séparation des préoccupations rendra le code plus propre, plus facile à lire et à maintenir. La logique de chaque format sera isolée.
- **Flexibilité** : L'utilisateur pourra choisir le format le plus adapté à son besoin, augmentant ainsi l'utilité du skill.
- **Testabilité** : Chaque module pourra être testé de manière indépendante.
