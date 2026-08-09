from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class BrowserPage:
    url: str
    title: str


class BrowserAdapter(Protocol):
    """Browser boundary. Concrete automation is implemented separately from AI routing."""

    name: str

    def open(self, url: str) -> BrowserPage:
        ...

    def current_page(self) -> BrowserPage | None:
        ...
