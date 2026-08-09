import argparse
import json

from zelda.app import brain


def main() -> None:
    parser = argparse.ArgumentParser(prog="zelda", description="Z.E.L.D.A. AI control service")
    parser.add_argument("command", nargs="*", help="Natural language command")
    args = parser.parse_args()

    text = " ".join(args.command).strip()
    if not text:
        text = input("Z.E.L.D.A. > ").strip()

    result = brain.handle(text)
    print(result.message)
    if result.data:
        print(json.dumps(result.data, indent=2, default=str))


if __name__ == "__main__":
    main()
