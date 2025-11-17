import requests
import base64
from datetime import datetime, timedelta

# Optional: cache token to reduce API calls
ACCESS_TOKEN = None
EXPIRES_AT = None

# Sandbox credentials
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


def get_access_token():
    """
    Get MPesa OAuth access token. Cache for reuse until expiry.
    """
    global ACCESS_TOKEN, EXPIRES_AT

    if ACCESS_TOKEN and EXPIRES_AT > datetime.now():
        return ACCESS_TOKEN

    # Encode credentials
    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(OAUTH_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")

    data = response.json()
    ACCESS_TOKEN = data["access_token"]
    expires_in = int(data.get("expires_in", 3600))
    EXPIRES_AT = datetime.now() + timedelta(seconds=expires_in - 60)  # 60 sec buffer

    return ACCESS_TOKEN
