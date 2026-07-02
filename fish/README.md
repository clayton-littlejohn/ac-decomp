# fish/ — Fish modding workspace

Tools and docs for extending the fish system in this Animal Crossing decomp.

| File | Purpose |
|---|---|
| [fish.md](fish.md) | Auto-generated reference table of every fish (prices, shadow sizes, spawn locations/times/months) — always matches the game code |
| [gen_fish_table.py](gen_fish_table.py) | Regenerates `fish.md` by parsing the real data tables in `src/` and `include/` (`--write` to save) |
| [gen_fish_model.py](gen_fish_model.py) | **Generates a complete 3D fish model** (swizzled CI4 texture + palette + 3-frame swim mesh) as a vanilla-style `act_f##` C file from a small color/shape spec |
| [make_iso.py](make_iso.py) | **One-shot pipeline**: `ninja` build → dialog/mail patches → inject rebuilt code → final bootable ISO |
| [build_test_iso.py](build_test_iso.py) | Lower-level: inject an already-built `foresta.rel.szs` into an ISO (used when you don't want the full pipeline) |
| [setup_dolphin_test_keys.py](setup_dolphin_test_keys.py) | One-shot Dolphin setup: binds the **P key** to the in-game test cheat (give a neon tetra while the inventory is open); `--remove` to uninstall |
| [ADDING_FISH.md](ADDING_FISH.md) | Step-by-step checklist for adding a new, fully-functional fish (enum → item → price → model → spawns → encyclopedia → house tank) |

## Quick start

```bash
python fish/make_iso.py         # build + patch + pack -> build/GAFE01_00/Animal Crossing (USA) (final).iso
python fish/make_iso.py --run   # ...and boot it in Dolphin
```

Useful flags: `--skip-build` (reuse last build), `--skip-dialog`, `--iso`/`--out`
to change source/destination, `--dolphin "C:\path\to\Dolphin.exe"`.

Other commands:

```bash
python fish/gen_fish_table.py --write  # refresh fish/fish.md from game code
ninja                                  # build only (sha1 CHECK failure = expected for mods)
```

## What's implemented

- **Fish encyclopedia page 2**: clicking the blue fish tab while the fish page
  is open plays the normal tab transition and flips to a second 40-slot page
  (azure-recolored window). The paging generalizes to N pages via
  `mIV_FISH_PAGE_NUM`.
- **Fish #41 "Neon tetra"** (worked example): catchable in rivers on summer
  nights, custom inventory icon, sellable (2,000 Bells), encyclopedia page 2,
  releasable. Uses the vanilla guppy 3D model for now; a generated custom model
  and a placeable house tank exist in the tree but are parked pending art
  iteration (see ADDING_FISH.md). A temporary test cheat puts a tetra in pocket
  slot 1 and unlocks its encyclopedia entry every time the inventory opens
  (`mIV_MOD_FISH_TEST_CHEAT` in src/game/m_inventory_ovl.c).
