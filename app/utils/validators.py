import re

# -------------------------------
# Email Validation
# -------------------------------
def is_valid_email(email: str) -> bool:
    """
    Checks if the email has a valid format.
    """
    if not email:
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# -------------------------------
# Phone Number Validation (Kenya)
# -------------------------------
def is_valid_phone(phone: str) -> bool:
    """
    Checks if the phone number is valid (Kenyan format).
    Accepts +2547XXXXXXXX or 07XXXXXXXX
    """
    if not phone:
        return False
    pattern = r"^(?:\+254|0)?7\d{8}$"
    return re.match(pattern, phone) is not None


# -------------------------------
# Amount Validation
# -------------------------------
def is_valid_amount(amount) -> bool:
    """
    Ensure amount is numeric and positive.
    """
    try:
        amt = float(amount)
        return amt > 0
    except (TypeError, ValueError):
        return False


# -------------------------------
# Password Validation
# -------------------------------
def is_valid_password(password: str) -> bool:
    """
    Ensure password has minimum 8 characters, at least
    one uppercase letter, one lowercase, one digit.
    """
    if not password or len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True
