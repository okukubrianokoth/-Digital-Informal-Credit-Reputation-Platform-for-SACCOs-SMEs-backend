import os
import requests
import base64
from datetime import datetime, timedelta

# Optional: cache token to reduce API calls
ACCESS_TOKEN = None
EXPIRES_AT = None


def get_access_token():
    """
    Get MPesa OAuth access token. Reads credentials from environment variables:
      - MPESA_CONSUMER_KEY
      - MPESA_CONSUMER_SECRET
      - MPESA_OAUTH_URL (optional, defaults to sandbox)

    Caches the token until expiry. Raises a clear error if credentials are missing.
    """
    global ACCESS_TOKEN, EXPIRES_AT

    if ACCESS_TOKEN and EXPIRES_AT and EXPIRES_AT > datetime.now():
        return ACCESS_TOKEN

    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    oauth_url = os.getenv(
        "MPESA_OAUTH_URL",
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
    )

    if not consumer_key or not consumer_secret:
        raise RuntimeError(
            "MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET must be set in the environment"
        )

    # Encode credentials
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(oauth_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")

    data = response.json()
    ACCESS_TOKEN = data.get("access_token")
    expires_in = int(data.get("expires_in", 3600))
    EXPIRES_AT = datetime.now() + timedelta(seconds=expires_in - 60)  # 60 sec buffer

    return ACCESS_TOKEN
