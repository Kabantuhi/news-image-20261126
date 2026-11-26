#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261126 (stdlib only, no network).

Copies the repository's entry.png to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png), after validating it is a whole PNG of
at most 1 MiB and exactly 1024 by 1024 pixels. Deterministic: the same
bytes in, the same bytes out.
"""
import os
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > 1048576:
        sys.exit("entry.png is over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    # IHDR: width/height are bytes 16..24 (big-endian uint32).
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        sys.exit("entry.png is %dx%d, expected 1024x1024" % (width, height))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    with open(out, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
