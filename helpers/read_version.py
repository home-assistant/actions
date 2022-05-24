from __future__ import annotations

import configparser
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def main() -> int:
    """Read version from setup.cfg or pyproject file passed as first argument."""
    argv = sys.argv[1:]

    if (len(argv) < 1 or not Path(argv[0]).is_file()):
        return 1

    if Path(argv[0]).name == "setup.cfg":
        parser = configparser.ConfigParser()
        parser.read(argv[0])

        print(parser["metadata"]["version"])
        return 0

    if Path(argv[0]).name == "pyproject.toml":
        with open(argv[0], "rb") as fp:
            data = tomllib.load(fp)

        print(data["project"]["version"])
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
