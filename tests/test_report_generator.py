import os
import pytest
from report_generator import generate_html_report

def test_generate_html_report(tmp_path):
    results = ["Result 1", "Result 2"]
    output_path = tmp_path / "report.html"
    generate_html_report(results, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "<h1>Code Review Report</h1>" in content
    assert "<li>Result 1</li>" in content
    assert "<li>Result 2</li>" in content