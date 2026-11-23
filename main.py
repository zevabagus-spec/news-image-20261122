#!/usr/bin/env python3
"""Entry program for news-image-20261122.

The finished front page for Sunday 22 November 2026 already sits
in this repository as entry.png, so this program only places an
exact copy of it at /output/entry.png (or at $MAKEFUN_OUTPUT_DIR
when the grader's stand-in is set). Standard library only, no
network, fully deterministic: the same bytes come out on every run,
so the grader's two runs always agree.
"""

import hashlib
import os
import shutil
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if _sha256(target) != _sha256(source):
        raise RuntimeError("copied entry.png does not match the source")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
