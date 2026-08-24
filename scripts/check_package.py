"""Verify the released wheel includes the public typed register surface."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "cyrisk_register/__init__.py",
    "cyrisk_register/models.py",
    "cyrisk_register/engine.py",
    "cyrisk_register/py.typed",
}


def main() -> int:
    wheels = sorted((ROOT / "dist").glob("cyrisk_register-*.whl"))
    if len(wheels) != 1:
        print(f"expected one wheel, found {len(wheels)}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(wheels[0]) as archive:
        missing = REQUIRED - set(archive.namelist())
    if missing:
        print(f"wheel missing files: {sorted(missing)}", file=sys.stderr)
        return 1
    print(f"VALID wheel={wheels[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
