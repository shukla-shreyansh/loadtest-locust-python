import os

RAMP_UP = float(os.getenv('RAMP_UP', '60'))
RAMP_DOWN = float(os.getenv('RAMP_DOWN', '60'))
TOKEN_FILE = os.getenv('TOKEN_FILE')
TOKEN = os.getenv('TOKEN')
TEST_DURATION = 60

# config/loader.py
import json

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def load_apis():
    return load_json_file('apis.json')

def load_payloads():
    return load_json_file('payloads.json')