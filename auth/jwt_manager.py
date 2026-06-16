from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from config import JWT_ALGORITHM, JWT_EXPIRATION_HOURS, JWT_SECRET


def create_token(payload: Dict[str, Any]) -> str:
    data = dict(payload)
    data["exp"] = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
