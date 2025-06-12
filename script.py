import os
import json
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import datetime

from utils import collect_valid_files, calculate_token_count, split_large_file
from bedrock_client import invoke_model_with_retry
from report_generator import generate_html_report

def main():
    """Main function to parse arguments and start the code review workflow."""
    parser = argparse.ArgumentParser(description="Automate code reviews using Amazon Bedrock.")
    parser.add_argument("--project-dir", required=True, help="Path to the project directory containing code.")
    parser.add_argument("--languages", nargs='+', required=True, help="Languages to review (e.g., python, java).")
    parser.add_argument("--app-name", required=True, help="Name of the application being reviewed.")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed debug logs.")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/{args.app_name}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    report_content = []

    for language in args.languages:
        config_file = f"configs/languages/{language.lower()}.json"
        if not os.path.exists(config_file):
            logging.warning("No configuration found for %s. Skipping.", language)
            continue

        with open(config_file, "r") as f:
            config = json.load(f)

        if "model_id" not in config:
            logging.error("'model_id' not found in config file: %s. Skipping %s.", config_file, language)
            continue

        valid_files = list(collect_valid_files(args.project_dir, config["valid_extensions"], config["excluded_directories"]))
        if not valid_files:
            logging.warning("No valid files found for %s. Skipping.", language)
            continue

        # Read file contents before submitting to the model
        file_contents = []
        for file_path in valid_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_contents.append(f.read())
            except (OSError, IOError, UnicodeDecodeError) as e:
                logging.warning("Could not read %s: %s", file_path, e)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(invoke_model_with_retry, config["model_id"], content) for content in file_contents]
            for future in tqdm(futures, desc=f"Processing {language}"):
                report_content.append(future.result())

    try:
        with open(os.path.join(output_dir, "report.json"), "w", encoding="utf-8") as f:
            json.dump(report_content, f, indent=4)
    except IOError as e:
        logging.error("Failed to write report: %s", e)

if __name__ == "__main__":
    main()
