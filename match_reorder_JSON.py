import json
from datetime import datetime
import os
import sys

# Base folder where this script lives (works in IDE and when bundled with PyInstaller)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)

# Paths
JSON_DIR = os.path.join(BASE_DIR, "json")
MATCHES_PATH = os.path.join(JSON_DIR, "matches.json")

# Ensure folder exists
os.makedirs(JSON_DIR, exist_ok=True)

# Ensure file exists and is valid JSON
if not os.path.exists(MATCHES_PATH):
    with open(MATCHES_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_matches():
    try:
        with open(MATCHES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # Corrupted file — reset to empty list
        with open(MATCHES_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    except FileNotFoundError:
        with open(MATCHES_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

def save_matches(matches):
    with open(MATCHES_PATH, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)

class MatchRecorder:
    def __init__(self, file_path=None):
        # Allow overriding for tests; default uses the canonical path
        self.file = file_path or MATCHES_PATH

    def record(self, color, difficulty, result, moves):
        entry = {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "player_color": color,
            "difficulty": difficulty,
            "result": result,
            "moves": moves,
        }

        if self.file == MATCHES_PATH:
            matches = load_matches()
            matches.append(entry)
            save_matches(matches)
        else:
            matches = _load_custom(self.file)
            matches.append(entry)
            _save_custom(self.file, matches)

# Helper functions for optional custom file paths
def _load_custom(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    except FileNotFoundError:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

def _save_custom(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)