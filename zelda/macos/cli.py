from __future__ import annotations

import json

from zelda.macos.system import MacOSSystemCapabilities


def main() -> None:
    print("Z.E.L.D.A. macOS runtime")
    print(json.dumps(MacOSSystemCapabilities.system_info([]), indent=2))
    print("Installed applications:")
    for name in MacOSSystemCapabilities.app_list([]):
        print(f"  {name}")


if __name__ == "__main__":
    main()
