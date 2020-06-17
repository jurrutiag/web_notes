import sys
from pathlib import Path
import json

SETTINGS = Path(__file__).resolve().parent / 'notes' / 'allowed_hosts.json'

if __name__ == "__main__":
    ip = sys.argv[1]

    with open(SETTINGS, 'r') as f:
        json_file = json.load(f)
        json_file['ALLOWED_HOSTS'] = [ip]

    with open(SETTINGS, 'w') as f:
        json.dump(json_file, f)
