from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def clean_text(value: str) -> str:
    return (value or "").strip()
