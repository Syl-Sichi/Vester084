from __future__ import annotations

import platform


def startup_message() -> str:
    host = platform.system()
    if host == "Darwin":
        return "Z.E.L.D.A. starting on macOS"
    if host == "Linux":
        return "Z.E.L.D.A. starting on Linux"
    return f"Z.E.L.D.A. starting on {host}"


def launch() -> None:
    print(startup_message())
    from zelda.cli import main
    main()


if __name__ == "__main__":
    launch()
