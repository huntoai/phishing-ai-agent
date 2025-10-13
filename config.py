"""
Configuration constants for the phishing AI agent.
"""
from datetime import timedelta

# AI Model Configuration
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
MAX_RETRIES = 2

# Cache Durations
CACHE_DURATION_TRENDS = timedelta(hours=24)
CACHE_DURATION_REGIONAL = timedelta(days=30)
CACHE_DURATION_INDUSTRY = timedelta(hours=12)

# API Timeouts (seconds)
API_TIMEOUT_DEFAULT = 10
API_TIMEOUT_SEARCH = 15
API_TIMEOUT_LINKEDIN = 20

# Search Configuration
SEARCH_MAX_RESULTS = 10
SEARCH_FRESHNESS = "pm"  # past month

# Email Configuration
DEFAULT_EMAIL_MODE = "simulation"
DEFAULT_SENDER_DOMAIN = "securemail.test"
DEFAULT_SENDER_NAME = "IT Security"
DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_USE_TLS = True

# Database Configuration
DATABASE_URL = "sqlite:///phishing_agent.db"

# Logging Configuration
LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Rate Limiting
LINKEDIN_RATE_LIMIT_STATUS = 999  # LinkedIn anti-scraping response code
