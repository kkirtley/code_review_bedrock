
# Utility functions for processing files and splitting content
import os
from typing import List, Generator

def collect_valid_files(directory: str, valid_extensions: List[str], excluded_dirs: List[str]) -> Generator[str, None, None]:
    """Recursively collects files with valid extensions, excluding specified directories."""
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        # Modify the dirs list in-place to exclude specified directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        # Iterate over the files in the current directory
        for file in files:
            # Check if the file has one of the valid extensions
            if any(file.endswith(ext) for ext in valid_extensions):
                # Yield the full path of the valid file
                yield os.path.join(root, file)

def calculate_token_count(content: str) -> int:
    """Estimates the token count for the given content."""
    return len(content.split())

def split_large_file(file_path: str, token_limit: int) -> List[str]:
    """Splits file content into smaller chunks that fit within the token limit."""
    chunks = []
    try:
        with open(file_path, 'r') as file:
            tokens = []
            for line in file:
                tokens.extend(line.split())
                while len(tokens) >= token_limit:
                    chunks.append(" ".join(tokens[:token_limit]))
                    tokens = tokens[token_limit:]
            if tokens:
                chunks.append(" ".join(tokens))
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while processing the file {file_path}.")
    return chunks
