# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests<3",
#     "rich",
#     "pandas",
#     "matplotlib",
#     "seaborn",
# ]
# ///
import os
import re
import pandas as pd
import json
import requests
import sys
import warnings

warnings.filterwarnings("ignore")

def load_dataset(file_path):
    """Load the dataset from a CSV file, ignoring malformed characters."""
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        return df
    except Exception as e:
        raise ValueError(f"Failed to load dataset: {e}")

def dataset_details(df):
    """Extract the dataset details to be sent to the OpenAI API."""
    details = {
        "name": input_file,
        "shape": df.shape,
        "columns": dict(zip(df.columns, df.dtypes.astype(str))),
        "missing_values": df.isnull().sum().to_dict(),
        "summary_statistics": df.describe(include='all').to_dict()
    }
    if len(df.columns) > 1:
        details["correlations"] = df.corr(numeric_only=True).to_dict()
    return details

def interact_with_openai(prompt, api_key):
    """Interact with OpenAI API to generate Python code."""
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a Python coder helping to generate Python code for dataset analysis and visualizations."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise RuntimeError(f"OpenAI API request failed: {e}")

def clean_generated_code(generated_code):
    """Clean the response from OpenAI to extract only valid Python code."""
    # Remove code block syntax (like markdown)
    cleaned_code = re.sub(r'```(?:python)?(.*?)```', r'\1', generated_code, flags=re.DOTALL)
    
    # Remove any comments or explanations that might be included in the response
    cleaned_code = re.sub(r'\b(?:Explain|Note|Instruction|Comment):?.*$', '', cleaned_code, flags=re.MULTILINE)  # Removes lines that are instructions
    
    # Remove extra spaces or newlines at the beginning or end
    cleaned_code = cleaned_code.strip()
    
    return cleaned_code

def generate_code_and_execute(df, api_key):
    """Send dataset details to OpenAI and execute the returned code."""
    details = dataset_details(df)
    
    # Prepare prompt to ask the LLM for the appropriate code
    prompt = (
        f"Here is a dataset with the following summary:\n"
        f"File Name: {input_file}\n"
        f"Shape: {details['shape']}\n"
        f"Columns: {json.dumps(details['columns'])}\n"
        f"Missing values: {json.dumps(details['missing_values'])}\n"
        f"Summary statistics: {json.dumps(details['summary_statistics'])}\n"
        f"Correlations: {json.dumps(details.get('correlations', {}))}\n"
        "Write Python code to analyze this dataset and generate visualizations, including histograms and a correlation heatmap."
        "The code should save the images as PNG files (e.g., 'histogram.png', 'heatmap.png') and generate a README.md file with a brief description of the dataset and results of your automated analysis, written as a story."
        "Also, use 'ISO 8859-1' as the dataset may contain diacritics and use only the numbered columns to create charts."
        "Keep images small. 512x512 px images are ideal. That's the size of 1 tile. Or, send detail: low to reduce cost"
        "The code must be ready for execution without requiring any manual corrections."
        "The response should only include the code and no other text as it's directly passed into the exec() function."
    )
    
    try:
        generated_code = interact_with_openai(prompt, api_key)

        cleaned_code = clean_generated_code(generated_code)

        exec(cleaned_code)
    except RuntimeError as e:
        print(f"Error generating or executing code: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    input_file = sys.argv[1]

    api_key = os.getenv("AIPROXY_TOKEN")

    if not api_key:
        print("Error: OpenAI API key is not set. Please set the api_key environment variable.")
        sys.exit(1)

    try:
        df = load_dataset(input_file)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Generate code and execute it
    generate_code_and_execute(df, api_key)
