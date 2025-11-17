# Gexbot v2 Historical Data Downloader

This Python script queries the Gexbot v2 API to retrieve download links for historical data.

## Overview

This script (`main.py`) is configured to query the Gexbot v2 historical data endpoints. It will iterate through a user-defined list of tickers and data categories ("combos") for a specific date.

For each valid combination, the script will print a JSON response to the console. This JSON object contains a **`url`** key. You can copy and paste this URL into your browser to download the corresponding historical data file.

## Configuration

Before running, you must configure the script:

### 1. Set Your API Key

The script requires a valid Gexbot API key. You can set this in one of two ways:

* **(Recommended)** As an environment variable named `GEXBOT_API_KEY`.
* **Alternatively**, you can paste your key directly into the `API_KEY` variable in `main.py`:

    ```python
    # main.py
    API_KEY = "YOUR_API_KEY_HERE"
    ```

### 2. Set the Query Date

Change the `DATE_TO_QUERY` variable to the `YYYY-MM-DD` date you wish to retrieve.

```python
# main.py
DATE_TO_QUERY = "2025-11-14"