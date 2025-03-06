"""
Dynamically generated capability: fetch_current_bitcoin_price
"""

import requests
from typing import Dict, Union, Tuple
from datetime import datetime

def fetch_current_bitcoin_price() -> Tuple[Union[float, str], str]:
    """
    Fetches the current Bitcoin spot price in USD from a reliable cryptocurrency API.
    
    Returns:
        Tuple[Union[float, str], str]: A tuple containing:
            - The current BTC/USD exchange rate as a float or string
            - A timestamp string of when the data was retrieved
    
    Raises:
        ConnectionError: If there's an issue connecting to the API
        ValueError: If the API response cannot be parsed
        Exception: For any other unexpected errors
    """
    try:
        # Using CoinGecko API as a reliable source for Bitcoin price data
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_last_updated_at": True
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        
        # Extract price and validate response format
        if "bitcoin" not in data or "usd" not in data["bitcoin"]:
            raise ValueError("Unexpected API response format")
        
        btc_price = float(data["bitcoin"]["usd"])
        
        # Generate timestamp for when we received the data
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return btc_price, current_timestamp
        
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to Bitcoin price API: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Failed to parse Bitcoin price data: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching Bitcoin price: {str(e)}")