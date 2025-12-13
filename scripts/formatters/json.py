import json


def save_report(data: dict, output_path: str) -> bool:
    """
    Sauvegarde le dictionnaire d'analyse au format JSON.
    Args:
        data: Dictionnaire contenant l'analyse structurée.
        output_path: Chemin vers le fichier JSON de sortie.
    Returns:
        True si succès, False sinon
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Fichier généré: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du fichier JSON: {e}")
        return False
