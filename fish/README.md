# fish/ — Fish modding workspace

Tools and docs for extending the fish system in this Animal Crossing decomp.

| File | Purpose |
|---|---|
| [fish.md](fish.md) | Auto-generated reference table of every fish (prices, shadow sizes, spawn locations/times/months) — always matches the game code |
| [gen_fish_table.py](gen_fish_table.py) | Regenerates `fish.md` by parsing the real data tables in `src/` and `include/` (`--write` to save) |
| [make_iso.py](make_iso.py) | **One-shot pipeline**: `ninja` build → dialog/mail patches → inject rebuilt code → final bootable ISO |
| [build_test_iso.py](build_test_iso.py) | Lower-level: inject an already-built `foresta.rel.szs` into an ISO (used when you don't want the full pipeline) |
| [ADDING_FISH.md](ADDING_FISH.md) | Step-by-step checklist for adding a new, fully-functional fish (enum → item → price → assets → spawns → encyclopedia) |

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
  (empty circles until fish are registered in `mIV_fish_collect_list2[]`,
  `src/game/m_inventory_ovl.c`). Clicking again returns to page 1. The paging
  generalizes to N pages via `mIV_FISH_PAGE_NUM`.
