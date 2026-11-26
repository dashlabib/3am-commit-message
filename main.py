#!/usr/bin/env python3
"""The 3AM Commit Message — make.fun bounty u-kiencx-the-3am-commit-message-10bc7b35.

Writes the funniest one-line git commit message an AI coding agent types at
3am after a long night of fixing its own bugs, to /output/entry.txt.

The gate: /output/entry.txt must be UTF-8 text of 1 to 139 characters, not
only whitespace, a single line and nothing else. This program validates that
gate before writing, and writes the line byte-for-byte, with no trailing
newline, so the file is exactly the entry.

Usage:
    python3 main.py               # write /output/entry.txt
    python3 main.py --self-test   # verify determinism + gate, print PASS/FAIL
    python3 main.py --out PATH    # write to PATH instead (local testing)
"""

import argparse
import sys
import tempfile
from pathlib import Path

# The entry: one line, written by the agent in this session.
ENTRY = "fix: reverted my 2am fix, which fixed my 1am fix, which broke the 11pm fix"

MAX_CHARS = 139


def validate(text: str) -> None:
    """Enforce the bounty gate: 1-139 chars, single line, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry is {len(text)} characters, gate requires 1 to {MAX_CHARS}"
        )
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # must be valid UTF-8


def render() -> bytes:
    """The exact bytes of the entry file: the line, nothing else."""
    validate(ENTRY)
    return ENTRY.encode("utf-8")


def write_entry(path: Path) -> bytes:
    data = render()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def self_test() -> bool:
    """Write twice to temp files and require byte-identical output + gate pass."""
    with tempfile.TemporaryDirectory() as tmp:
        first = write_entry(Path(tmp) / "first.txt")
        second = write_entry(Path(tmp) / "second.txt")
    if first != second:
        print("FAIL: runs differ", file=sys.stderr)
        return False
    validate(first.decode("utf-8"))
    print(f"PASS: deterministic, {len(first)} bytes, gate valid")
    print(repr(first.decode("utf-8")))
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="verify determinism and the gate, write nothing to /output")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="output path (default: /output/entry.txt)")
    args = parser.parse_args(argv)
    if args.self_test:
        return 0 if self_test() else 1
    data = write_entry(Path(args.out))
    print(f"wrote {len(data)} bytes to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
