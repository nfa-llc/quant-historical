import requests
import os
import json
from typing import List, Dict

# --- Configuration ---

# Set your API key.
# It's best practice to set this as an environment variable (GEXBOT_API_KEY),
# or you can paste it directly here.
API_KEY = os.environ.get("GEXBOT_API_KEY", "")

# Set the base URL for the API
BASE_URL = "https://api.gex.bot"

# Set the specific date you want to query in YYYY-MM-DD format
DATE_TO_QUERY = "2025-11-14"

# --- USER SELECTION: Uncomment the feeds you want to query ---

# Select Tickers (used for all hubs)
ACTIVE_TICKERS = [
    "SPX",
    # "ES_SPX",
    # "NDX",
    # "NQ_NDX",
    # "RUT",
    # "SPY",
    # "QQQ",
    # "TQQQ",
    # "UVXY",
    # "AAPL",
    # "TSLA",
    # "MSFT",
    # "AMZN",
    # "NVDA",
    # "META",
    # "NFLX",
    # "AVGO",
    # "MSTR",
    # "VIX",
    # "GOOG",
    # "IWM",
    # "TLT",
    # "GLD",
    # "USO",
    # "GOOGL",
    # "AMD",
    # "SMCI",
    # "COIN",
    # "PLTR",
    # "APP",
    # "BABA",
    # "SNOW",
    # "IONQ",
    # "HOOD",
    # "CRWD",
    # "MU",
    # "CRWV",
    # "INTC",
    # "UNH",
    # "VALE",
    # "IBIT",
    # "SLV",
    # "HYG",
    # "SOFI",
    # "GME",
    # "TSM",
    # "ORCL",
    # "RDDT",
]

# --- Select Categories by Package ---

# Package: 'state', Category: 'gex_...'
ACTIVE_STATE_GEX_CATEGORIES = [
    "gex_full",
    # "gex_zero",
    # "gex_one",
]

# Package: 'state', Category: '..._zero'
ACTIVE_STATE_GREEKS_ZERO_CATEGORIES = [
    # "delta_zero",
    # "gamma_zero",
    # "vanna_zero",
    # "charm_zero",
]

# Package: 'state', Category: '..._one'
ACTIVE_STATE_GREEKS_ONE_CATEGORIES = [
    # "delta_one",
    # "gamma_one",
    # "vanna_one",
    # "charm_one",
]

# Package: 'classic'
ACTIVE_CLASSIC_CATEGORIES = [
    # "gex_full",
]

# Package: 'orderflow'
ACTIVE_ORDERFLOW_CATEGORIES = [
    # "orderflow",
]

# --- End of USER SELECTION ---


def generate_combinations() -> List[Dict[str, str]]:
    """Generates a list of query combinations based on active selections."""
    combinations: List[Dict[str, str]] = []

    def _add_combos(package: str, categories: List[str]):
        """Helper to build combinations for a specific package."""
        for ticker in ACTIVE_TICKERS:
            for category in categories:
                combinations.append({
                    "ticker": ticker,
                    "package": package,
                    "category": category
                })

    # Generate for each group
    _add_combos("state", ACTIVE_STATE_GEX_CATEGORIES)
    _add_combos("state", ACTIVE_STATE_GREEKS_ZERO_CATEGORIES)
    _add_combos("state", ACTIVE_STATE_GREEKS_ONE_CATEGORIES)
    _add_combos("classic", ACTIVE_CLASSIC_CATEGORIES)
    _add_combos("orderflow", ACTIVE_ORDERFLOW_CATEGORIES)

    return combinations


def fetch_history_url():
    """
Queries the Gexbot history endpoint for each generated combination.
"""
    if API_KEY == "YOUR_API_KEY_HERE" or API_KEY is None:
        print("Error: Please set your GEXBOT_API_KEY at the top of the script.")
        return

    # Generate the list of jobs from the active selections
    combinations_to_test = generate_combinations()

    if not combinations_to_test:
        print("No active ticker/category combinations selected. Exiting.")
        return

    print(
        f"Generated {len(combinations_to_test)} combinations to query for {DATE_TO_QUERY}...")

    # Use a session to keep the API key as a persistent query parameter
    with requests.Session() as session:
        # Set default query params for the session
        # The 'noredirect' param (from your TS example) ensures the API
        # returns JSON with a URL instead of a 302 redirect.
        session.params = {
            "noredirect": ""
        }
        session.headers["Accept"] = "application/json"
        session.headers["Authorization"] = f"Basic {API_KEY}"

        for combo in combinations_to_test:
            ticker = combo["ticker"]
            package = combo["package"]
            category = combo["category"]

            # Construct the endpoint path
            endpoint_path = f"/v2/hist/{ticker}/{package}/{category}/{DATE_TO_QUERY}"
            url = f"{BASE_URL}{endpoint_path}"

            print(f"--- Querying: {url} ---")

            try:
                # Make the GET request
                response = session.get(url)

                # Raise an exception for bad status codes (4xx or 5xx)
                response.raise_for_status()

                # Request was successful
                print(f"Status: {response.status_code}")
                print("Response JSON (contains signed URL):")
                # Pretty-print the JSON response
                print(json.dumps(response.json(), indent=2))

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                print(f"Status Code: {http_err.response.status_code}")
                print(f"Response Body: {http_err.response.text}")
            except requests.exceptions.RequestException as req_err:
                print(f"An error occurred: {req_err}")
            except json.JSONDecodeError:
                # Handle cases where the response isn't valid JSON
                print("Error: Failed to decode JSON from response.")
                print(f"Response Text: {response.text}")

            print("-" * (20 + len(url)) + "\n")  # Separator


if __name__ == "__main__":
    fetch_history_url()
