# Store API keys here
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
BASE_URL = "https://api.alpaca.markets"
