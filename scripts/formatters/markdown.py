def format_fallacies(fallacies: list) -> str:
    """Format fallacies list to string, supporting both string and dict formats."""
    if not fallacies:
        return "Aucun détecté"

    result = []
    for f in fallacies:
        if isinstance(f, str):
            result.append(f)
        elif isinstance(f, dict):
            name = f.get("name", "Inconnu")
            severity = f.get("severity", "")
            if severity:
                result.append(f"{name} ({severity})")
            else:
                result.append(name)

    return ", ".join(result) if result else "Aucun détecté"


def save_report(data: dict, output_path: str) -> bool:
    """
    Génère un rapport Markdown à partir du dictionnaire d'analyse.
    Args:
        data: Dictionnaire contenant l'analyse structurée.
        output_path: Chemin vers le fichier Markdown de sortie.
    Returns:
        True si succès, False sinon
    """
    markdown_content = []

    # Metadata
    metadata = data.get("metadata", {})
    markdown_content.append(f"# Analyse Rhétorique: {metadata.get('title', 'Non spécifié')}")
    markdown_content.append(f"**Source:** {metadata.get('source', 'Non spécifié')}")
    markdown_content.append(f"**Date d'analyse:** {metadata.get('date_analysis', 'Non spécifié')}")
    markdown_content.append(f"**Analyste:** {metadata.get('analyst', 'Non spécifié')}\n")

    # Synthesis
    synthesis = data.get("synthesis", {})
    markdown_content.append("## Synthèse Critique")
    markdown_content.append("### Points forts:")
    for strength in synthesis.get("strengths", []):
        markdown_content.append(f"- {strength}")
    markdown_content.append("\n### Points faibles:")
    for weakness in synthesis.get("weaknesses", []):
        markdown_content.append(f"- {weakness}")
    markdown_content.append("\n### Figures rhétoriques récurrentes:")
    for pattern in synthesis.get("recurring_patterns", []):
        markdown_content.append(f"- {pattern}")
    markdown_content.append(f"\n### Note méthodologique:\n{synthesis.get('methodological_note', '')}\n")

    # Arguments Analysis
    markdown_content.append("## Analyse Détaillée des Arguments")
    for arg in data.get("arguments", []):
        markdown_content.append(f"### Argument N°{arg.get('id', '')}: {arg.get('label', '')}")
        markdown_content.append(f"**Texte original (extrait):**\n> {arg.get('original_text', '')}\n")
        markdown_content.append(f"**Thèse (Claim):** {arg.get('claim', '')}")
        markdown_content.append(f"**Type de raisonnement:** {arg.get('reasoning_type', '')}")
        markdown_content.append(f"**Sophismes détectés:** {format_fallacies(arg.get('fallacies', []))}")
        markdown_content.append(f"**Fiabilité (1-5):** {arg.get('reliability', 3)}")
        markdown_content.append(f"**Évaluation de la fiabilité:** {arg.get('reliability_rationale', '')}")
        markdown_content.append(f"**Commentaire:** {arg.get('comment', '')}\n")

        markdown_content.append("#### Détail Toulmin")
        markdown_content.append(f"- **Grounds:** {arg.get('grounds', '')}")
        markdown_content.append(f"- **Warrant:** {arg.get('warrant', '')}")
        markdown_content.append(f"- **Backing:** {arg.get('backing', 'Non explicité')}")
        markdown_content.append(f"- **Qualifier:** {arg.get('qualifier', 'Non explicité')}")
        markdown_content.append(f"- **Rebuttal:** {arg.get('rebuttal', 'Non reconnu')}\n")

        if arg.get("sources_cited"):
            markdown_content.append("#### Sources Citées (CRAAP)")
            markdown_content.append("| Source | Currency | Relevance | Authority | Accuracy | Purpose | Score moyen |")
            markdown_content.append("|---|---|---|---|---|---|---|")
            for source in arg.get("sources_cited", []):
                craap = source.get("craap_score", {})
                scores = [
                    craap.get("currency", 0),
                    craap.get("relevance", 0),
                    craap.get("authority", 0),
                    craap.get("accuracy", 0),
                    craap.get("purpose", 0)
                ]
                avg_score = sum(scores) / len(scores) if scores else 0
                markdown_content.append(
                    f"| {source.get('name', '')} "
                    f"| {scores[0]} | {scores[1]} | {scores[2]} | {scores[3]} | {scores[4]} "
                    f"| {round(avg_score, 1)} |"
                )
            markdown_content.append("\n")

    # Legend
    markdown_content.append("## Légende")
    markdown_content.append("### Échelle de Fiabilité")
    markdown_content.append("| Note | Niveau | Description |")
    markdown_content.append("|---|---|---|")
    legend = [
        (5, "Très haute", "Fait établi, consensus scientifique, sources multiples vérifiables"),
        (4, "Bonne", "Sources sérieuses, raisonnement logique valide, nuances possibles"),
        (3, "Moyenne", "Mélange faits/interprétations, sources partielles"),
        (2, "Faible", "Raisonnement contestable, sophismes identifiés"),
        (1, "Très faible", "Affirmations non sourcées, erreurs logiques majeures"),
    ]
    for note, niveau, desc in legend:
        markdown_content.append(f"| {note} | {niveau} | {desc} |")

    markdown_content.append("\n### Critères CRAAP")
    markdown_content.append("| Critère | Description |")
    markdown_content.append("|---|---|")
    craap_criteria = [
        ("Currency", "L'information est-elle à jour ?"),
        ("Relevance", "L'information est-elle pertinente pour le propos ?"),
        ("Authority", "L'auteur/source est-il crédible dans ce domaine ?"),
        ("Accuracy", "Les faits sont-ils vérifiables et exacts ?"),
        ("Purpose", "Quelle est l'intention ? (informer, persuader, vendre...)"),
    ]
    for critere, desc in craap_criteria:
        markdown_content.append(f"| {critere} | {desc} |")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        print(f"✅ Fichier généré: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du fichier Markdown: {e}")
        return False