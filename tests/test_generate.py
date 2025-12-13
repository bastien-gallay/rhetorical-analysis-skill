"""Tests pour le générateur d'analyse rhétorique."""

import json
import subprocess

# Import the main script to test its CLI functionality
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts import generate_analysis


@pytest.fixture
def example_analysis_json_path():
    """Fixture for the path to the example analysis JSON."""
    return Path("assets/example_analysis.json")

@pytest.fixture
def minimal_analysis_data():
    """Fixture with a minimal valid analysis data."""
    return {
        "metadata": {
            "title": "Test Article",
            "source": "https://example.com",
            "date_analysis": "2025-12-12",
            "analyst": "Test Analyst"
        },
        "arguments": [
            {
                "id": 1,
                "label": "Test argument",
                "original_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "claim": "Test claim",
                "grounds": "Test grounds",
                "warrant": "Test warrant",
                "reasoning_type": "Deductive",
                "fallacies": [],
                "reliability": 4,
                "reliability_rationale": "Well sourced",
                "sources_cited": [],
                "comment": "A critical comment."
            }
        ],
        "synthesis": {
            "strengths": ["Good sourcing"],
            "weaknesses": ["Missing context"],
            "recurring_patterns": ["Appeal to authority"],
            "methodological_note": "Test note"
        }
    }

@pytest.fixture
def minimal_analysis_json_file(minimal_analysis_data, tmp_path):
    """Fixture that creates a temporary JSON file with minimal analysis data."""
    json_path = tmp_path / "minimal_analysis.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(minimal_analysis_data, f)
    return json_path

class TestGenerateAnalysisCLI:
    """Tests pour l'interface en ligne de commande de generate_analysis.py."""

    def test_cli_xlsx_output(self, minimal_analysis_json_file, tmp_path):
        """Vérifie que le CLI génère correctement un fichier XLSX."""
        output_xlsx = tmp_path / "report.xlsx"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(minimal_analysis_json_file),
                str(output_xlsx),
                "--format", "xlsx"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Stdout: {result.stdout}, Stderr: {result.stderr}"
        assert output_xlsx.exists()
        assert output_xlsx.stat().st_size > 0 # Ensure file is not empty

    def test_cli_json_output(self, minimal_analysis_json_file, tmp_path):
        """Vérifie que le CLI génère correctement un fichier JSON."""
        output_json = tmp_path / "report.json"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(minimal_analysis_json_file),
                str(output_json),
                "--format", "json"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Stdout: {result.stdout}, Stderr: {result.stderr}"
        assert output_json.exists()
        assert output_json.stat().st_size > 0
        # Validate JSON content
        with open(output_json, encoding='utf-8') as f:
            loaded_data = json.load(f)
        with open(minimal_analysis_json_file, encoding='utf-8') as f:
            original_data = json.load(f)
        assert loaded_data == original_data

    def test_cli_markdown_output(self, minimal_analysis_json_file, tmp_path):
        """Vérifie que le CLI génère correctement un fichier Markdown."""
        output_md = tmp_path / "report.md"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(minimal_analysis_json_file),
                str(output_md),
                "--format", "md"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Stdout: {result.stdout}, Stderr: {result.stderr}"
        assert output_md.exists()
        assert output_md.stat().st_size > 0
        # Check for some expected content in the Markdown file
        content = output_md.read_text()
        assert "# Analyse Rhétorique: Test Article" in content
        assert "## Synthèse Critique" in content
        assert "### Argument N°1: Test argument" in content
        assert "| Note | Niveau | Description |" in content

    def test_cli_missing_arguments(self):
        """Vérifie le comportement avec des arguments manquants."""
        result = subprocess.run(
            [sys.executable, str(generate_analysis.__file__)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 2
        assert "input_file" in result.stderr
        assert "output_file" in result.stderr

    def test_cli_invalid_input_file(self, tmp_path):
        """Vérifie le comportement avec un fichier d'entrée non existant."""
        output_xlsx = tmp_path / "report.xlsx"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(Path("non_existent.json")),
                str(output_xlsx)
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Fichier non trouvé" in result.stdout

    def test_cli_invalid_json_content(self, tmp_path):
        """Vérifie le comportement avec un fichier JSON malformé."""
        invalid_json_file = tmp_path / "invalid.json"
        invalid_json_file.write_text("{ invalid json }")
        output_xlsx = tmp_path / "report.xlsx"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(invalid_json_file),
                str(output_xlsx)
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Le fichier JSON d'entrée est invalide" in result.stdout

    def test_cli_unsupported_format(self, minimal_analysis_json_file, tmp_path):
        """Vérifie le comportement avec un format de sortie non supporté."""
        output_file = tmp_path / "report.xyz"
        result = subprocess.run(
            [
                sys.executable,
                str(generate_analysis.__file__),
                str(minimal_analysis_json_file),
                str(output_file),
                "--format", "xyz"
            ],
            capture_output=True,
            text=True
        )
        assert result.returncode == 2 # argparse exits with 2 for invalid choices
        assert "invalid choice: 'xyz'" in result.stderr
