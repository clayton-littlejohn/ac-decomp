# fish/ — Fish modding workspace

Tools and docs for extending the fish system in this Animal Crossing decomp.

| File | Purpose |
|---|---|
| [fish.md](fish.md) | Auto-generated reference table of every fish (prices, shadow sizes, spawn locations/times/months) — always matches the game code |
| [add_fish.py](add_fish.py) | **THE mass-add workflow**: declare fish in `FISH_SPECS` (name, price, size, spawn months/times/area, icon recolor, model reuse) and it patches all ~14 code touchpoints automatically, idempotently |
| [gen_fish_table.py](gen_fish_table.py) | Regenerates `fish.md` by parsing the real data tables in `src/` and `include/` (`--write` to save) |
| [gen_fish_model.py](gen_fish_model.py) | Generates a complete 3D fish model (swizzled CI4 texture + palette + 3-frame swim mesh) as a vanilla-style `act_f##` C file from a small color/shape spec |
| [make_iso.py](make_iso.py) | **One-shot pipeline**: `ninja` build → dialog/mail patches → inject rebuilt code → final bootable ISO |
| [build_test_iso.py](build_test_iso.py) | Lower-level: inject an already-built `foresta.rel.szs` into an ISO |
| [setup_dolphin_test_keys.py](setup_dolphin_test_keys.py) | Optional Dolphin key binding for test cheats; `--remove` to uninstall |
| [ADDING_FISH.md](ADDING_FISH.md) | The underlying per-file checklist (what add_fish.py automates) |
| [CUSTOM_FISH_ASSET_WORKFLOW.md](CUSTOM_FISH_ASSET_WORKFLOW.md) | Preview-first workflow for vanilla-consistent custom fish icons and catch/held/release models |

For custom non-reskin fish art, use the preview-first workflow in
[CUSTOM_FISH_ASSET_WORKFLOW.md](CUSTOM_FISH_ASSET_WORKFLOW.md). It documents
how to generate vanilla-base icon candidates, choose one beside the fish grid,
then install the approved icon and matching catch/held/release model.

## Adding fish (mass workflow)

```bash
# 1. add entries to FISH_SPECS in fish/add_fish.py, then:
python fish/add_fish.py               # patches all code touchpoints (idempotent)
python fish/gen_fish_table.py --write # refresh fish.md
python fish/make_iso.py               # build + pack final ISO
```

Current state: **80 fish** (40 vanilla + tetra + 39 more) — encyclopedia page 2 is
full; the next fish requires a third page (`mIV_FISH_PAGE_NUM` + `mIV_fish_collect_list3`,
add_fish.py will refuse until then). Neon tetra is the worked example for replacing
both placeholder asset classes: it uses a generated custom catch/release model and
a dedicated inventory/encyclopedia icon texture. The remaining modded fish still
reuse vanilla model/icon shapes until they get their own generated assets.

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
  nights, custom inventory/encyclopedia icon texture, sellable (2,000 Bells),
  encyclopedia page 2, releasable, and wired to a generated custom low-poly
  catch/release model. A placeable house tank exists in the tree but remains
  separate from the catch/release work (see ADDING_FISH.md). A temporary test
  cheat puts a tetra in pocket slot 1 and unlocks its encyclopedia entry every
  time the inventory opens (`mIV_MOD_FISH_TEST_CHEAT` in src/game/m_inventory_ovl.c).
