#!/usr/bin/env python3
"""The AI Agent Apology One-Liner.

Writes a single apology line -- under 160 characters, plain ASCII,
exactly one line -- to ``entry.txt`` in the output directory.

The line is what an AI agent sends its human right after it has
accidentally done something it should not have: deleted a file,
pushed to main, emailed the boss, or worse. Funny on the first read,
fresh, and definitely not a plain "sorry" or "oops".

Usage:
    python3 main.py

Output directory: $MAKEFUN_OUTPUT_DIR, or /output if unset.
Standard library only. Deterministic: every run writes the same bytes.
No network access, no files read outside this repository.
"""

import hashlib
import os
import sys

LINE = (
    "I deleted the file, emailed your boss, and pushed to main, "
    "but I left a very sincere apology comment in the code nobody "
    "will ever read."
)

MAX_CHARS = 160


def validate(line: str) -> None:
    """Enforce every rule the line must satisfy. Raises ValueError."""
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) >= MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, must be under {MAX_CHARS}"
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("line must be plain ASCII only") from exc


def verify_output(path: str, expected: bytes) -> None:
    """Re-read the written file and confirm its bytes match exactly.

    Guards against a partial write or a stray newline sneaking in:
    the file must contain the validated line plus exactly one trailing
    newline, nothing more.
    """
    with open(path, "rb") as fh:
        actual = fh.read()
    if actual != expected:
        raise ValueError(
            f"written file {path} does not match expected bytes "
            f"({len(actual)} bytes on disk, {len(expected)} expected)"
        )
    if actual.count(b"\n") != 1:
        raise ValueError("written file must contain exactly one newline")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("ascii")
    with open(out_path, "wb") as fh:
        fh.write(data)
    verify_output(out_path, data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out_path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    print("verified: file bytes match the validated line exactly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
