import json
import os
from typing import Dict, List, Any

def load_json_file(filename: str) -> Any:
    """
    Load a JSON file and return its contents.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        Any: The contents of the JSON file.

    Raises:
        FileNotFoundError: If the specified file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON.")
        raise

def load_apis() -> List[Dict[str, str]]:
    """
    Load the API configurations from the apis.json file.

    Returns:
        List[Dict[str, str]]: A list of API configurations.
    """
    return load_json_file('apis.json')

def load_payloads() -> Dict[str, List[Dict[str, Any]]]:
    """
    Load the payload configurations from the payloads.json file.

    Returns:
        Dict[str, List[Dict[str, Any]]]: A dictionary of payload configurations.
    """
    return load_json_file('payloads.json')

def get_payload_for_api(api_name: str) -> Dict[str, Any]:
    """
    Get a random payload for the specified API.

    Args:
        api_name (str): The name of the API.

    Returns:
        Dict[str, Any]: A random payload for the specified API.

    Raises:
        KeyError: If no payloads are defined for the specified API.
    """
    import random

    payloads = load_payloads()
    try:
        return random.choice(payloads[api_name])
    except KeyError:
        print(f"Warning: No payloads defined for API '{api_name}'. Using empty payload.")
        return {}

def validate_config_files():
    """
    Validate that the necessary configuration files exist.

    Raises:
        FileNotFoundError: If any of the required configuration files are missing.
    """
    required_files = ['apis.json', 'payloads.json']
    for file in required_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required configuration file '{file}' is missing.")

# Validate configuration files when this module is imported
validate_config_files()