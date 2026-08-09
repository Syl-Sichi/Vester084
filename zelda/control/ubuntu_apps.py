from __future__ import annotations

import os
from pathlib import Path


class UbuntuApplicationCapabilities:
    """Read only discovery of applications and running processes."""

    @staticmethod
    def app_list(args: list[str]) -> list[str]:
        roots = (Path("/usr/share/applications"), Path.home() / ".local/share/applications")
        apps: set[str] = set()
        for root in roots:
            if not root.is_dir():
                continue
            for desktop_file in root.glob("*.desktop"):
                try:
                    text = desktop_file.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for line in text.splitlines():
                    if line.startswith("Name="):
                        name = line[5:].strip()
                        if name:
                            apps.add(name)
                        break
        return sorted(apps, key=str.casefold)

    @staticmethod
    def app_find(args: list[str]) -> list[str]:
        query = " ".join(args).strip().casefold()
        if not query:
            raise ValueError("application_query_required")
        return [name for name in UbuntuApplicationCapabilities.app_list([]) if query in name.casefold()]

    @staticmethod
    def app_status(args: list[str]) -> dict[str, object]:
        query = " ".join(args).strip().casefold()
        if not query:
            raise ValueError("application_query_required")
        matches: list[dict[str, object]] = []
        proc_root = Path("/proc")
        for entry in proc_root.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                comm = (entry / "comm").read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                continue
            if query in comm.casefold():
                matches.append({"pid": int(entry.name), "name": comm})
        return {"query": query, "running": bool(matches), "processes": matches}
