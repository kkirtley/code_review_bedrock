import os
import pytest
import subprocess

def test_code_review_main(tmp_path):
    # Setup
    project_dir = tmp_path / "project"
    os.makedirs(project_dir)
    (project_dir / "test.py").write_text("print('Hello, world!')")
    config_dir = tmp_path / "configs"
    os.makedirs(config_dir)
    (config_dir / "python.json").write_text('{"valid_extensions": [".py"], "excluded_directories": [], "max_tokens": 4000, "model_id": "test_model"}')
    
    # Run the main function
    result = subprocess.run(["python", "code_review.py", "--project-dir", str(project_dir), "--languages", "python", "--app-name", "test_app"], capture_output=True, text=True)
    
    # Check the output
    assert result.returncode == 0
    output_dir = tmp_path / "output"
    assert output_dir.exists()
    assert any(output_dir.glob("test_app_*.json"))
    assert any(output_dir.glob("test_app_*.html"))