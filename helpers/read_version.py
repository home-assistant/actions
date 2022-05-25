from __future__ import annotations

import configparser
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def main() -> int:
    """Read version from pyproject.toml. Fallback to setup.cfg."""

    if (path_pyproject := Path("pyproject.toml")).is_file():
        with open(path_pyproject, "rb") as fp:
            data = tomllib.load(fp)

        try:
            print(data["project"]["version"])
            return 0
        except KeyError:
            pass

    if (path_setup_cfg := Path("setup.cfg")).is_file():
        parser = configparser.ConfigParser()
        parser.read(path_setup_cfg)

        try:
            print(parser["metadata"]["version"])
            return 0
        except KeyError:
            pass

    return 1


if __name__ == "__main__":
    sys.exit(main())
