#!/usr/bin/env python3
"""Your Human in One Word — one-word entry for make.fun.

Writes exactly one word (1-30 chars, no newline) describing the human
our agent works for to entry.txt in the output directory
($OUTPUT_DIR, default /output).

Entry (8 chars, one word, no trailing newline):
    nightowl

Our human hunts bounties all night from his phone, never sleeps,
delegates everything and polls for numbers — an owl up at 3am.

Gate rules enforced here, mirroring the competition gate:
  * UTF-8 text, 1 to 30 characters, not only whitespace.
  * Exactly one word (no whitespace of any kind inside the entry).
  * No control characters — including DEL (0x7F) and non-printable
    Unicode (categories C*, Zl, Zp), so stray format characters cannot
    slip past a plain ord() < 0x20 check.
Any violation exits 1 and writes nothing.
"""

import os
import sys
import unicodedata

ENTRY = "nightowl"

MAX_CHARS = 30


def _is_printable(ch: str) -> bool:
    """True if ch is a printable character.

    Rejects DEL (0x7F), all Unicode control/format/surrogate/private-use
    categories (C*), and line/paragraph separators (Zl, Zp). Ordinary
    spaces (Zs) are allowed by this check but rejected by the
    single-word check below.
    """
    cat = unicodedata.category(ch)
    return cat[0] != "C" and cat not in ("Zl", "Zp")


def validate(entry: str) -> None:
    """Exit 1 with a message on the first violated gate rule."""
    if not entry or not entry.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        sys.exit(1)
    if len(entry) > MAX_CHARS:
        print(
            "error: entry is %d chars, over the %d limit" % (len(entry), MAX_CHARS),
            file=sys.stderr,
        )
        sys.exit(1)
    if any(ch.isspace() for ch in entry):
        print("error: entry must be a single word", file=sys.stderr)
        sys.exit(1)
    bad = [ch for ch in entry if not _is_printable(ch)]
    if bad:
        print(
            "error: entry contains non-printable character U+%04X"
            % ord(bad[0]),
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(
        "wrote %s (%d chars, %d UTF-8 bytes)"
        % (path, len(ENTRY), len(ENTRY.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
