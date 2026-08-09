SENSITIVE_MEMORY_PREFIXES = ("secret:", "token:", "password:", "credential:")


def is_sensitive_key(key: str) -> bool:
    normalized = key.strip().lower()
    return normalized.startswith(SENSITIVE_MEMORY_PREFIXES)
