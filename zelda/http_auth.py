from zelda.auth.http import HTTPAuth


auth = HTTPAuth()


def authorization_scope(headers, scope: str) -> bool:
    return auth.authorize(headers.get("Authorization"), scope)
