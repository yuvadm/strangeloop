"""
Dynamically generated capability: get_public_ip_address
"""

import requests
from typing import Optional


def get_public_ip_address() -> Optional[str]:
    """
    Retrieves the public IP address of the current machine by calling httpbin.org/ip.
    
    Returns:
        Optional[str]: The public IP address as a string if successful, None otherwise.
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request.
        ValueError: If the response format is unexpected.
    """
    try:
        response = requests.get("https://httpbin.org/ip", timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        if "origin" not in data:
            raise ValueError("Unexpected response format from httpbin.org/ip")
        
        return data["origin"]
    except requests.RequestException as e:
        # Log the error or handle it as needed
        print(f"Error retrieving public IP address: {e}")
        return None
    except ValueError as e:
        # Log the error or handle it as needed
        print(f"Error parsing response: {e}")
        return None