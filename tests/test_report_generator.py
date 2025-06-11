""" Tests for the report_generator module. """
from pathlib import Path
from report_generator import generate_html_report

def test_generate_html_report(tmp_path: Path):
    """
    Test the generate_html_report function.
    This test verifies that the generate_html_report function correctly creates
    an HTML report file with the given results.
    Args:
        tmp_path (Path): A temporary directory path provided by pytest.
    Assertions:
        - The output HTML file is created at the specified path.
        - The content of the HTML file includes the expected header and list items.
    """
    results = ["Result 1", "Result 2"]
    output_path = tmp_path / "report.html"
    generate_html_report(results, output_path)
    assert output_path.exists()
    content = output_path.read_text()
    assert "<h1>Code Review Report</h1>" in content
    assert "<li>Result 1</li>" in content
    assert "<li>Result 2</li>" in content
