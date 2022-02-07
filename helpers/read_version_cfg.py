from __future__ import annotations

import configparser
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Read version from setup.cfg file passed as first argument."""
    argv = argv or sys.argv[1:]

    parser = configparser.ConfigParser()
    if (len(argv) < 1 or not Path(argv[0]).is_file()):
        return 1
    parser.read(argv[0])

    print(parser["metadata"]["version"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
