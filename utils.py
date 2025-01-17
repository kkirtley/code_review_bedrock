
# Utility functions for processing files and splitting content
import os
from typing import List, Generator

def collect_valid_files(directory: str, valid_extensions: List[str], excluded_dirs: List[str]) -> Generator[str, None, None]:
    """Recursively collects files with valid extensions, excluding specified directories."""
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                yield os.path.join(root, file)

def calculate_token_count(content: str) -> int:
    """Estimates the token count for the given content."""
    return len(content.split())

def split_large_file(content: str, token_limit: int) -> List[str]:
    """Splits file content into smaller chunks that fit within the token limit."""
    tokens = content.split()
    return [" ".join(tokens[i:i + token_limit]) for i in range(0, len(tokens), token_limit)]
