#!/usr/bin/env python3
"""make_iso.py — ONE command to produce the final patched, bootable ISO.

Pipeline:
  1. ``ninja``                 - compile the modded game code (a sha1 CHECK
                                 failure on foresta.rel is expected and ignored;
                                 any real compile/link error aborts).
  2. dialog patches            - applies dialog/dialog.json + dialog/mail.json
                                 via tools/dialog_tool.py (skipped if absent).
  3. code injection            - swaps the rebuilt foresta.rel.szs into the ISO.

Usage (from repo root):
    python fish/make_iso.py            # -> build/GAFE01_00/Animal Crossing (USA) (final).iso
    python fish/make_iso.py --run      # ...and boot it in Dolphin

Options:
    --iso PATH       source ISO (default: orig/GAFE01_00/Animal Crossing (USA).iso)
    --out PATH       output ISO
    --skip-build     don't run ninja (use existing build artifacts)
    --skip-dialog    don't apply dialog/mail patches
    --run            launch Dolphin on the result
    --dolphin PATH   Dolphin executable (default: "Dolphin" on PATH)
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import gcm  # noqa: E402

DEFAULT_ISO = REPO / "orig" / "GAFE01_00" / "Animal Crossing (USA).iso"
DEFAULT_OUT = REPO / "build" / "GAFE01_00" / "Animal Crossing (USA) (final).iso"
BUILT_REL_SZS = REPO / "build" / "GAFE01_00" / "foresta" / "foresta.rel.szs"
DIALOG_TOOL = REPO / "tools" / "dialog_tool.py"
DIALOG_JSONS = [REPO / "dialog" / "dialog.json", REPO / "dialog" / "mail.json"]


def step(msg: str) -> None:
    print(f"\n=== {msg} ===")


def run_ninja() -> None:
    """Run ninja; tolerate a failure only if it is the sha1 CHECK step."""
    step("1/3 build (ninja)")
    proc = subprocess.run(["ninja"], cwd=REPO, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.strip())
    if proc.returncode != 0:
        failed = [ln for ln in out.splitlines() if ln.startswith("FAILED")]
        only_check = failed and all(("/ok" in ln or "build.sha1" in ln) for ln in failed)
        if not only_check:
            sys.exit("error: build failed (see output above)")
        print("note: only the retail sha1 CHECK failed - expected for a mod, continuing")


def apply_dialog(src: Path, out: Path) -> Path:
    jsons = [j for j in DIALOG_JSONS if j.exists()]
    step("2/3 dialog patches")
    if not jsons or not DIALOG_TOOL.exists():
        print("no dialog patch files found - skipping")
        return src
    cmd = [sys.executable, str(DIALOG_TOOL), "apply-iso", "--iso", str(src),
           "--json", *[str(j) for j in jsons], "--out", str(out)]
    print("running:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    subprocess.run(cmd, cwd=REPO, check=True)
    return out


def inject_rel(iso_path: Path) -> None:
    step("3/3 inject rebuilt game code (foresta.rel.szs)")
    if not BUILT_REL_SZS.exists():
        sys.exit(f"error: {BUILT_REL_SZS} not found - build first (drop --skip-build)")
    disc = gcm.Gcm(iso_path)
    gf = disc.find("foresta.rel.szs")
    if gf is None:
        sys.exit("error: foresta.rel.szs not found in ISO filesystem")
    new_rel = BUILT_REL_SZS.read_bytes()
    print(f"foresta.rel.szs: disc {gf.size:,} bytes -> built {len(new_rel):,} bytes")
    disc.replace_files([(gf, new_rel)], iso_path)  # in-place


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--iso", type=Path, default=DEFAULT_ISO)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--skip-build", action="store_true")
    ap.add_argument("--skip-dialog", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--dolphin", default="Dolphin")
    args = ap.parse_args()

    if not args.iso.exists():
        sys.exit(f"error: source ISO not found: {args.iso}")

    if not args.skip_build:
        run_ninja()
    else:
        step("1/3 build (ninja) - skipped")

    args.out.parent.mkdir(parents=True, exist_ok=True)

    if not args.skip_dialog:
        patched = apply_dialog(args.iso, args.out)
        if patched != args.out:  # dialog step skipped itself; start from source ISO
            shutil.copyfile(args.iso, args.out)
    else:
        step("2/3 dialog patches - skipped")
        shutil.copyfile(args.iso, args.out)

    inject_rel(args.out)

    print(f"\ndone: {args.out}")

    if args.run:
        exe = shutil.which(args.dolphin) or args.dolphin
        print(f"launching: {exe}")
        subprocess.Popen([exe, str(args.out)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
