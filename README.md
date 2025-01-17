# Code Review Automation with Amazon Bedrock

## Overview

This project automates code review for multiple programming languages using Amazon Bedrock. It processes files in a specified project directory, evaluates them against language-specific standards, and generates comprehensive reports, including JSON and HTML summaries, error logs, and batch results.

---

## Features

- **Multi-Language Support**: Review Python, JavaScript, Java, and C# files in a single run.
- **Customizable Configurations**: Language-specific standards, token limits, and batch sizes can be adjusted through configuration files.
- **Dynamic Output Handling**: Each run generates a timestamped directory for output files.
- **Parallel Processing**: Optimized for faster processing with parallel execution.
- **Error Logging**: Detailed error logs for debugging issues in specific files or batches.
- **Rate Limiting and Retries**: Automatically handles Bedrock API rate limits and retries transient errors.

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher.
- An AWS account with access to Amazon Bedrock.
- Install the required Python libraries listed in `requirements.txt`.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/code-review-bedrock.git
   cd code-review-bedrock
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment
   ```
   python3 -m venv .venv
   ```

### AWS Configuration

Ensure AWS credentials are configured either through environment variables or in `~/.aws/credentials`.

---

## Usage

Run the script using the following command:

```bash
python main.py --project-dir /path/to/project --languages python java javascript --app-name my_app
```

- `--project-dir`: Path to the project directory containing files to review.
- `--languages`: Space-separated list of languages to review (e.g., python, java).
- `--app-name`: Name of the application being reviewed.
- `--verbose`: (Optional) Enables detailed debug logs.

---

## Configuration

Configuration files are stored in the `configs/` directory. Each file specifies:

- Model ID
- Token limits
- Batch sizes
- Standards for review
- Valid file extensions
- Excluded directories

Example configuration for Python (`configs/python.json`):

```json
{
  "model_id": "amazon.titan-your-model-id",
  "batch_size": 5,
  "token_limit": 4000,
  "standards": "Task: Review the following Python code for adherence to best practices...",
  "valid_extensions": [".py"],
  "excluded_directories": ["__pycache__", "venv", "build"]
}
```

---

## Outputs

Reports are saved in a timestamped subdirectory under `output/`. Output files include:

1. **JSON Report**: A comprehensive report with responses for each batch.
2. **HTML Report**: A user-friendly version of the JSON report.
3. **Error Logs**: Details of errors encountered during processing.
4. **Summary File**: High-level statistics about the run.

---

## Contributions

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---
