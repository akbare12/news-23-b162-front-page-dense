#!/usr/bin/env python3
"""news-23 b162 front-page-dense entry runner (stdlib only, no PIL).

Verifies the bundled entry.png (1024x1024 PNG, <=1 MiB, valid chunks/CRCs)
and copies it to $MAKEFUN_OUTPUT_DIR/entry.png. The grader runs this from a
read-only copy, so it must never write next to main.py.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "515a5bb4bcc2985b0beaa013df60dea17b68dba674714c56f3ccb73e32c548de"
EXPECTED_SIZE = 157782

SRC_NAME = "entry.png"
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def read_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, "bad PNG signature"
    if len(data) < MIN_SIZE:
        return None, "file too small (%d bytes)" % len(data)
    if len(data) > MAX_SIZE:
        return None, "file too big (%d bytes)" % len(data)
    # Walk chunks: first must be a 13-byte IHDR for 1024x1024, 8-bit, colour
    # type 2 or 6, compression/filter/interlace all 0. CRC covers type+data.
    pos = 8
    first = True
    seen_iend = False
    idat_total = 0
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            return None, "truncated chunk %r" % ctype
        chunk_data = data[pos + 8:pos + 8 + length]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        crc_calc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            return None, "bad CRC in chunk %r" % ctype
        if first:
            if ctype != b"IHDR" or length != 13:
                return None, "first chunk must be a 13-byte IHDR"
            w, h, depth, ctype_n, comp, filt, inter = struct.unpack(
                ">IIBBBBB", chunk_data)
            if (w, h) != (1024, 1024):
                return None, "expected 1024x1024, got %dx%d" % (w, h)
            if depth != 8 or ctype_n not in (2, 6):
                return None, "unexpected bit depth / colour type"
            if comp != 0 or filt != 0 or inter != 0:
                return None, "unexpected compression/filter/interlace"
            # Explicit CRC check of the IHDR chunk itself.
            if zlib.crc32(b"IHDR" + chunk_data) & 0xFFFFFFFF != crc_stored:
                return None, "bad IHDR CRC"
            first = False
        if ctype == b"IDAT":
            if length == 0:
                return None, "empty IDAT chunk"
            idat_total += length
        if ctype == b"IEND":
            if length != 0:
                return None, "IEND must be empty"
            if pos + 12 + length != len(data):
                return None, "trailing data after IEND"
            seen_iend = True
            break
        pos += 12 + length
    if first:
        return None, "no IHDR chunk found"
    if not seen_iend:
        return None, "no IEND chunk found"
    if idat_total < 1000:
        return None, "IDAT payload too small"
    return data, None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    # Refuse to write into the repo itself or over the source file.
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % out_dir)
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: %s" % out_dir)
    data, err = read_png(src)
    if err is not None:
        return fail(err)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail("size mismatch: got %d, expected %d" % (len(data), EXPECTED_SIZE))
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source image")
    with open(dst, "wb") as f:
        f.write(data)
    # Re-read the output and confirm it is byte-identical to the source.
    with open(dst, "rb") as f:
        out_data = f.read()
    if out_data != data:
        return fail("output is not byte-identical to the source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
