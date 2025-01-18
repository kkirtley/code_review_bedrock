import os
import pytest
from utils import collect_valid_files, calculate_token_count, split_large_file

def test_collect_valid_files(tmp_path):
    # Setup
    valid_extensions = ['.py']
    excluded_dirs = ['excluded']
    os.makedirs(tmp_path / 'excluded')
    valid_file = tmp_path / 'test.py'
    valid_file.write_text("print('Hello, world!')")
    invalid_file = tmp_path / 'test.txt'
    invalid_file.write_text("Hello, world!")
    
    # Test
    files = list(collect_valid_files(tmp_path, valid_extensions, excluded_dirs))
    assert len(files) == 1
    assert files[0] == str(valid_file)

def test_calculate_token_count():
    content = "This is a test content"
    assert calculate_token_count(content) == 5

def test_split_large_file(tmp_path):
    file_path = tmp_path / 'test.txt'
    file_path.write_text("This is a test content that will be split into smaller chunks")
    chunks = split_large_file(file_path, 5)
    assert len(chunks) == 3
    assert chunks[0] == "This is a test content"
    assert chunks[1] == "that will be split into"
    assert chunks[2] == "smaller chunks"