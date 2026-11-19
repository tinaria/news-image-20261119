"""THE WORLD front page: 50 stories of Thursday 19 November 2026.

Entrypoint: place the pre-rendered front-page image into the output
directory as entry.png. Deterministic, no network, no randomness.
"""

import hashlib
import os
import shutil
from pathlib import Path


def copy_verified(source: Path, destination: Path) -> str:
    """Copy source to destination, then confirm both files match by sha256."""
    shutil.copyfile(source, destination)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
    if source_hash != destination_hash:
        raise RuntimeError("sha256 mismatch after copy")
    return destination_hash


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    copy_verified(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
