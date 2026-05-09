import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from bot.logging_config import get_logger

# Initialize a logger for this module
log = get_logger(__name__)

# Base URL for Binance Futures Testnet API
BASE_URL = "https://testnet.binancefuture.com"

class BinanceClient:
    def __init__(self, api_key: str, secret: str):
        # Store API key and secret for authentication
        self.api_key = api_key
        self.secret = secret

        # Create a persistent HTTP session (better performance, keeps headers)
        self.session = requests.Session()

        # Add Binance-required header for authentication
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign(self, params: dict) -> dict:
        # Binance requires a timestamp in milliseconds for signed requests
        params["timestamp"] = int(time.time() * 1000)

        # Convert parameters into a query string (key=value&key2=value2)
        query = urlencode(params)

        # Create HMAC-SHA256 signature using the secret key over the query string
        params["signature"] = hmac.new(
            self.secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()

        # Return the signed parameters (with timestamp + signature added)
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        # First sign the request parameters
        params = self._sign(params)

        # Log the outgoing request for debugging
        log.debug(f"POST {endpoint} | params: {params}")

        try:
            # Send POST request to Binance API
            r = self.session.post(f"{BASE_URL}{endpoint}", params=params)

            # Raise an exception if response status is 4xx/5xx
            r.raise_for_status()

            # Log the JSON response for debugging
            log.debug(f"Response: {r.json()}")

            # Return parsed JSON response
            return r.json()

        except requests.exceptions.HTTPError as e:
            # Log HTTP errors (e.g., invalid signature, bad request)
            log.error(f"HTTP error: {e.response.text}")
            raise

        except requests.exceptions.RequestException as e:
            # Log network-related errors (e.g., timeout, connection issues)
            log.error(f"Network error: {e}")
            raise
