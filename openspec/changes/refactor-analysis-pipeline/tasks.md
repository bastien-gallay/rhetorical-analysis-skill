- [ ] **Étape 1: Refactorisation de la structure**
    - [ ] Créer un nouveau répertoire `scripts/formatters`.
    - [ ] Créer des fichiers vides `scripts/formatters/__init__.py`, `scripts/formatters/excel.py`, `scripts/formatters/json.py`, `scripts/formatters/markdown.py`.
    - [ ] Déplacer la logique de génération XLSX de `scripts/generate_analysis.py` vers `scripts/formatters/excel.py`.
        - La nouvelle fonction `formatters.excel.save_report(data: dict, output_path: str)` contiendra la logique.
    - [ ] Mettre à jour `scripts/generate_analysis.py` pour qu'il agisse comme un répartiteur ("dispatcher").
        - Il chargera le JSON.
        - Il appellera le bon formateur en fonction d'un nouvel argument `--format`.

- [ ] **Étape 2: Implémentation des nouveaux formateurs**
    - [ ] Implémenter la fonction `formatters.json.save_report(data: dict, output_path: str)` qui sauvegarde les données en JSON formaté.
    - [ ] Implémenter la fonction `formatters.markdown.save_report(data: dict, output_path: str)` qui génère un rapport Markdown complet.
        - Le rapport Markdown devra contenir toutes les informations présentes dans le rapport Excel, mais dans un format textuel.

- [ ] **Étape 3: Mise à jour du CLI**
    - [ ] Utiliser `argparse` dans `scripts/generate_analysis.py` pour gérer les arguments de la ligne de commande.
    - [ ] Ajouter un argument `input_file` (positionnel).
    - [ ] Ajouter un argument `output_file` (positionnel).
    - [ ] Ajouter une option `--format` avec les choix `['xlsx', 'json', 'md']` et `xlsx` comme valeur par défaut.

- [ ] **Étape 4: Mise à jour de la documentation et des tests**
    - [ ] Mettre à jour le docstring de `scripts/generate_analysis.py` pour refléter la nouvelle interface CLI.
    - [ ] Créer un nouveau fichier de test `tests/test_formatters.py`.
    - [ ] Ajouter des tests pour chaque formateur pour vérifier que les fichiers de sortie sont créés correctement.
    - [ ] Mettre à jour `tests/test_generate.py` pour tester la nouvelle interface CLI et le mécanisme de dispatch.
    - [ ] Mettre à jour `README.md` et `SKILL.md` si nécessaire pour documenter la nouvelle fonctionnalité.

- [ ] **Étape 5: Validation**
    - [ ] Exécuter `uv run ruff check .` et corriger les erreurs.
    - [ ] Exécuter `uv run pytest` et s'assurer que tous les tests passent.
    - [ ] Tester manuellement chaque format de sortie pour s'assurer de la qualité du rendu.
