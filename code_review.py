import os
import json
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from configs.models.amazon_titan_text_express_v1 import model_id, token_limit
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
    parser.add_argument("--verbose", action="store_true", default=False, help="Enable detailed debug logs.")
    parser.add_argument("--model-id", required=False, default=model_id, help="LLM Model ID to use for code review.")
    parser.add_argument_group("--textGenerationConfig", required=False, help="Text generation configuration.")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/{args.app_name}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    results = []
    default_max_tokens = token_limit

    for language in args.languages:
        config_file = f"configs/{language.lower()}.json"
        if not os.path.exists(config_file):
            logging.warning(f"No configuration found for {language}. Skipping.")
            continue

        with open(config_file, "r") as f:
            config = json.load(f)

        valid_files = list(collect_valid_files(args.project_dir, config["valid_extensions"], config["excluded_directories"]))
        if not valid_files:
            logging.warning(f"No valid files found for {language}. Skipping.")
            continue

        for file in valid_files:
            token_count = calculate_token_count(file)
            if token_count > token_limit:
                file_chunks = split_large_file(file, token_limit)
            else:
                file_chunks = [file]

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(invoke_model_with_retry, config["model_id"], chunk) for chunk in file_chunks]
                for future in tqdm(futures, desc=f"Processing {language}"):
                    try:
                        results.append(future.result())
                    except Exception as e:
                        logging.error(f"Error processing file: {e}")

    try:
        with open(os.path.join(output_dir, "report.json"), "w") as f:
            json.dump(results, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to write report: {e}")

    try:
        generate_html_report(results, os.path.join(output_dir, "report.html"))
    except Exception as e:
        logging.error(f"Failed to generate HTML report: {e}")

if __name__ == "__main__":
    main()