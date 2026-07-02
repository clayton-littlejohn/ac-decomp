#!/usr/bin/env python3
"""build_test_iso.py — Pack the rebuilt game code into a bootable test ISO.

The fish/encyclopedia code lives in ``foresta.rel`` (compressed on disc as
``foresta.rel.szs``). After ``ninja`` compiles it, this script injects the
fresh ``foresta.rel.szs`` into a copy of the original ISO so it can be booted
in Dolphin.

Usage (from repo root):
    ninja                          # build first (sha1 CHECK failure is fine)
    python fish/build_test_iso.py  # writes the modded ISO
    python fish/build_test_iso.py --run   # ...and launch it in Dolphin

Options let you point at a different source ISO (e.g. one that already has
dialog patches applied) or output path.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gcm  # noqa: E402

DEFAULT_ISO = REPO / "orig" / "GAFE01_00" / "Animal Crossing (USA).iso"
DEFAULT_OUT = REPO / "build" / "GAFE01_00" / "Animal Crossing (USA) (fish test).iso"
BUILT_REL_SZS = REPO / "build" / "GAFE01_00" / "foresta" / "foresta.rel.szs"
BUILT_DOL = REPO / "build" / "GAFE01_00" / "static.dol"


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--iso", type=Path, default=DEFAULT_ISO,
                    help="source ISO to patch (default: original USA ISO)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help="output ISO path")
    ap.add_argument("--run", action="store_true",
                    help="launch the result in Dolphin afterwards")
    ap.add_argument("--dolphin", default="Dolphin",
                    help="Dolphin executable name/path (default: Dolphin on PATH)")
    args = ap.parse_args()

    if not BUILT_REL_SZS.exists():
        sys.exit(f"error: {BUILT_REL_SZS} not found - run `ninja` first")
    if not args.iso.exists():
        sys.exit(f"error: source ISO not found: {args.iso}")

    disc = gcm.Gcm(args.iso)
    gf = disc.find("foresta.rel.szs")
    if gf is None:
        sys.exit("error: foresta.rel.szs not found in ISO filesystem")

    new_rel = BUILT_REL_SZS.read_bytes()
    print(f"foresta.rel.szs: disc {gf.size:,} bytes -> built {len(new_rel):,} bytes")
    disc.replace_files([(gf, new_rel)], args.out)
    print(f"wrote {args.out}")

    # The DOL is outside the FST; it normally does not change for fish mods.
    # If it ever does, patch it in place (same-size DOLs only).
    orig_dol_sha = None
    with open(args.iso, "rb") as f:
        f.seek(disc.dol_offset)
        # DOL max size check is overkill here; compare first 1 MiB fingerprint
        orig_dol_head = f.read(1 << 20)
    built_dol = BUILT_DOL.read_bytes() if BUILT_DOL.exists() else b""
    if built_dol and built_dol[: 1 << 20] != orig_dol_head[: len(built_dol[: 1 << 20])]:
        print("note: static.dol differs from the disc DOL - patching it in place")
        with open(args.out, "r+b") as f:
            f.seek(disc.dol_offset)
            f.write(built_dol)

    if args.run:
        exe = shutil.which(args.dolphin) or args.dolphin
        print(f"launching: {exe} {args.out}")
        subprocess.Popen([exe, str(args.out)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
