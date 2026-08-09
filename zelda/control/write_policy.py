from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WriteAuthorization:
    """Explicit authorization token required for a state changing capability."""

    capability: str
    confirmed: bool = False

    def require_confirmation(self, capability: str) -> None:
        if self.capability != capability:
            raise PermissionError("write_authorization_mismatch")
        if not self.confirmed:
            raise PermissionError("write_confirmation_required")


def require_write_authorization(capability: str, authorization: WriteAuthorization | None) -> None:
    if authorization is None:
        raise PermissionError("write_confirmation_required")
    authorization.require_confirmation(capability)
