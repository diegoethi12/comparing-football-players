from datetime import datetime


def today_str(format: str) -> str:
    return datetime.utcnow().strftime(format)
