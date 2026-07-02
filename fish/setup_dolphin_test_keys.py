#!/usr/bin/env python3
"""setup_dolphin_test_keys.py — bind the fish test cheat to the P key in Dolphin.

The in-game test cheat (see src/game/m_inventory_ovl.c, mIV_MOD_FISH_TEST_CHEAT)
triggers on CONTROLLER 2, C-stick UP while the inventory is open. This script
makes that press-able with the P key on your keyboard, with no manual Dolphin
configuration:

  1. installs a GCPad input profile that binds only C-Stick Up -> keyboard P
  2. installs a per-game settings INI for Animal Crossing (GAFE01) that
     - plugs a Standard Controller into port 2 (SIDevice1 = 6)
     - assigns the profile to port 2 (PadProfile2)

Nothing about your port-1 controls or other games is touched; the settings
apply only when GAFE01 is running.

Usage:
    python fish/setup_dolphin_test_keys.py            # auto-detect Dolphin dir
    python fish/setup_dolphin_test_keys.py --dolphin-dir "D:/Dolphin/User"
    python fish/setup_dolphin_test_keys.py --remove   # uninstall

Restart Dolphin afterwards. In-game: open the inventory and press P.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROFILE_NAME = "ac_fish_test"
GAME_INI = "GAFE01.ini"

PROFILE_BODY = """[Profile]
Device = DInput/0/Keyboard Mouse
C-Stick/Up = P
"""

GAME_INI_SECTIONS = {
    "Core": {"SIDevice1": "6"},
    "Controls": {"PadProfile2": PROFILE_NAME},
}


def find_dolphin_user_dir() -> Path | None:
    candidates = []
    home = Path.home()
    if os.name == "nt":
        candidates += [
            home / "Documents" / "Dolphin Emulator",
            Path(os.environ.get("APPDATA", "")) / "Dolphin Emulator",
        ]
    else:
        candidates += [
            home / ".local" / "share" / "dolphin-emu",
            home / "Library" / "Application Support" / "Dolphin",
        ]
    for c in candidates:
        if (c / "Config").is_dir():
            return c
    return None


def merge_game_ini(path: Path, remove: bool) -> None:
    """Merge (or remove) our keys into the per-game INI, preserving the rest."""
    lines: list[str] = []
    if path.exists():
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # strip our keys everywhere first
    our_keys = {k.lower() for sec in GAME_INI_SECTIONS.values() for k in sec}
    section = None
    kept: list[str] = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1]
            kept.append(ln)
            continue
        key = s.split("=", 1)[0].strip().lower() if "=" in s else None
        if section in GAME_INI_SECTIONS and key in our_keys:
            continue  # drop; re-added below unless removing
        kept.append(ln)

    if not remove:
        for sec, kv in GAME_INI_SECTIONS.items():
            # find existing section
            idx = next((i for i, ln in enumerate(kept) if ln.strip() == f"[{sec}]"), None)
            entries = [f"{k} = {v}" for k, v in kv.items()]
            if idx is None:
                if kept and kept[-1].strip():
                    kept.append("")
                kept.append(f"[{sec}]")
                kept.extend(entries)
            else:
                kept[idx + 1:idx + 1] = entries

    # drop empty file on remove
    text = "\n".join(kept).strip()
    if text:
        path.write_text(text + "\n", encoding="utf-8")
        print(f"{'updated' if not remove else 'cleaned'} {path}")
    elif path.exists():
        path.unlink()
        print(f"removed {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dolphin-dir", type=Path, default=None,
                    help="Dolphin user directory (contains Config/)")
    ap.add_argument("--remove", action="store_true", help="uninstall the binding")
    args = ap.parse_args()

    user_dir = args.dolphin_dir or find_dolphin_user_dir()
    if user_dir is None or not (user_dir / "Config").is_dir():
        sys.exit("error: could not find the Dolphin user directory - pass --dolphin-dir "
                 "(the folder containing Config/, e.g. Documents/Dolphin Emulator)")

    profile_dir = user_dir / "Config" / "Profiles" / "GCPad"
    profile_path = profile_dir / f"{PROFILE_NAME}.ini"
    game_ini_path = user_dir / "GameSettings" / GAME_INI

    if args.remove:
        if profile_path.exists():
            profile_path.unlink()
            print(f"removed {profile_path}")
        merge_game_ini(game_ini_path, remove=True)
        print("uninstalled - restart Dolphin")
        return 0

    profile_dir.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(PROFILE_BODY, encoding="utf-8")
    print(f"wrote {profile_path}")

    game_ini_path.parent.mkdir(parents=True, exist_ok=True)
    merge_game_ini(game_ini_path, remove=False)

    print("\nDone. Restart Dolphin, boot the modded ISO, open your inventory")
    print("(Start) and press P to receive a neon tetra.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
