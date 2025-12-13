import json

import pytest

import scripts.formatters.excel as excel
import scripts.formatters.json as json_formatter
import scripts.formatters.markdown as markdown


# Define a temporary directory for test outputs
@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path / "output"

# Define a fixture for the input analysis data
@pytest.fixture
def example_analysis_data():
    with open("assets/example_analysis.json", encoding='utf-8') as f:
        return json.load(f)

# Test Excel formatter
def test_excel_formatter(example_analysis_data, temp_output_dir):
    output_path = temp_output_dir / "test_report.xlsx"
    success = excel.save_report(example_analysis_data, output_path)
    assert success is True
    assert output_path.exists()
    assert output_path.stat().st_size > 0 # Check if file is not empty

# Test JSON formatter
def test_json_formatter(example_analysis_data, temp_output_dir):
    output_path = temp_output_dir / "test_report.json"
    success = json_formatter.save_report(example_analysis_data, output_path)
    assert success is True
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    # Optionally, load and validate the JSON content
    with open(output_path, encoding='utf-8') as f:
        loaded_data = json.load(f)
    assert loaded_data == example_analysis_data

# Test Markdown formatter
def test_markdown_formatter(example_analysis_data, temp_output_dir):
    output_path = temp_output_dir / "test_report.md"
    success = markdown.save_report(example_analysis_data, output_path)
    assert success is True
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    # Optionally, read and check for some key content in Markdown
    content = output_path.read_text()
    assert "# Analyse Rhétorique:" in content
    assert "## Synthèse Critique" in content
    assert "### Argument N°1:" in content
    assert "| Note | Niveau | Description |" in content
