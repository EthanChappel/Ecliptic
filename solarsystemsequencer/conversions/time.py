def get_decimal(hours: int, minutes: int, seconds: int) -> float:
    return hours + (minutes / 60) + (seconds / 3600)
