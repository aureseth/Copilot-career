# Centralized configuration management

import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

# --- Path Configuration ---
# Build paths relative to this file's location
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"

# --- Load Environment Variables ---
# Load the .env file from the config directory
dotenv_path = CONFIG_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


# --- User Preferences ---
def load_preferences():
    """Loads user preferences from the YAML file."""
    preferences_path = CONFIG_DIR / "preferences.yaml"
    try:
        with open(preferences_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: '{preferences_path}' not found. Using default values.")
        return {}
    except Exception as e:
        print(f"Error loading preferences: {e}")
        return {}


PREFERENCES = load_preferences()

# --- Data Paths ---
MASTER_RESUME_PATH = DATA_DIR / "master_resume.pdf"

# --- Google API Config ---
# Scopes required for the application
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]
# Path to store the token created by the OAuth flow
GOOGLE_TOKEN_PATH = CONFIG_DIR / "token.json"
# Path for the credentials file downloaded from Google Cloud Console
GOOGLE_CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"


if __name__ == "__main__":
    # For testing the configuration loading
    print("--- Configuration Loaded ---")
    print(f"OpenAI Key Loaded: {bool(OPENAI_API_KEY)}")
    print(f"Notion Key Loaded: {bool(NOTION_API_KEY)}")
    print(f"Notion DB ID Loaded: {bool(NOTION_DATABASE_ID)}")
    print("\n--- Preferences ---")
    print(PREFERENCES)
    print("\n--- Paths ---")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Master Resume Path: {MASTER_RESUME_PATH}")
    print(f"Google Credentials Path: {GOOGLE_CREDENTIALS_PATH}")
