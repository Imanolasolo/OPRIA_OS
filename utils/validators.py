import re


_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]{3,40}$")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_username(value: str) -> bool:
    return bool(_USERNAME_PATTERN.match((value or "").strip()))


def is_valid_email(value: str) -> bool:
    return bool(_EMAIL_PATTERN.match((value or "").strip()))


def is_valid_password(value: str) -> bool:
    value = value or ""
    has_min_len = len(value) >= 8
    has_upper = any(char.isupper() for char in value)
    has_lower = any(char.islower() for char in value)
    has_digit = any(char.isdigit() for char in value)
    return has_min_len and has_upper and has_lower and has_digit
