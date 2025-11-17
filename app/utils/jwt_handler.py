from datetime import datetime, timedelta
import jwt
from flask import current_app

# -------------------------------
# Generate JWT Token
# -------------------------------
def create_token(identity: int, expires_in: int = 3600) -> str:
    """
    Create a JWT token with an expiry in seconds.
    identity: user id or unique identifier
    """
    payload = {
        "sub": identity,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token


# -------------------------------
# Decode JWT Token
# -------------------------------
def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return the payload.
    Raises exception if invalid or expired.
    """
    try:
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


# -------------------------------
# Verify Token
# -------------------------------
def verify_token(token: str) -> bool:
    """
    Returns True if token is valid, False otherwise.
    """
    try:
        decode_token(token)
        return True
    except Exception:
        return False
