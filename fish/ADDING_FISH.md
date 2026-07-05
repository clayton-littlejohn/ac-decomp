# Adding a New Fish — Complete Workflow

This document is the checklist for adding a brand-new, fully functional fish to
Animal Crossing (GameCube). **Fish #41, the Neon tetra, has been added using
exactly this process — search the codebase for `NEON_TETRA` / `modded` to see
every touchpoint as a worked example.** Follow it top to bottom; every step
maps to a real table in the decompiled source. After each addition, run
`python fish/gen_fish_table.py --write` to regenerate [fish.md](fish.md) and confirm
the game data matches your intent, then build with `python fish/make_iso.py`.

The engine identifies a fish two ways, and they diverge for modded fish:

* **fish/item index** — 0-39 vanilla, 40+ modded (`ITM_FISH_START + idx`)
* **gyo type** (`aGYO_TYPE_*`) — 0-39 vanilla fish, 40-44 whale/trash/salmon2,
  45+ modded fish

`aGYO_FISH_IDX_2_TYPE()` / `aGYO_TYPE_2_FISH_IDX()` in
[include/ac_gyoei.h](../include/ac_gyoei.h) convert between them. New fish are
appended **after** the whale/trash block so vanilla indices never move.

---

## Checklist (every file the Neon tetra touched)

| # | File | Change |
|---|------|--------|
| 1 | `include/ac_gyoei.h` | `aGYO_TYPE_<NAME>` after `aGYO_TYPE_EXTENDED_NUM`; bump `aGYO_TYPE_MODDED_NUM` |
| 2 | `src/actor/ac_gyoei_type.c_inc` | append `{ size, search_area, bite_time }` |
| 3 | `fish/gen_fish_model.py` | add a spec (colors/size) and run it → generates `src/data/model/act_f<NN>_<name>.c` (texture, palette, 3-frame swim mesh) |
| 4 | `src/actor/ac_gyoei_model.c_inc` | extern the generated models, add `aGYO_<name>_dl`, append to `aGYO_displayList` |
| 5 | `src/f_furniture.c` | `#include` the generated model file (compiles it into the build) |
| 6 | `src/actor/ac_uki_move.c_inc` | append item to `fish_data[]` |
| 7 | `src/actor/ac_gyo_release.c` | append to `aGYR_anime_ptn[]` (1 = small-fish wiggle, 2 = slow) |
| 8 | `include/m_name_table.h` | `#define ITM_FISH<n>`; bump `FISH_NUM`; append `X(FTR_MOD_FISH<nn>)` to the **FTR1 enum** |
| 9 | `include/m_ftr_def.h` | append `FTR_MOD_FISH<nn>` before `FTR_NUM` (kind enum; a compile-time check in `ac_mod_fish_tank.c` catches misalignment with #8) |
| 10 | `src/actor/ac_furniture_profile_data.c_inc` | append `&iam_mod_fish00` (profile is shared by all modded fish tanks) |
| 11 | `src/data/item/fish_price.c` | append catalog price before `-1` (sell = /4) |
| 12 | `src/data/item/item_name.c` | append 16-byte space-padded ASCII name after the `.inc` include |
| 13 | `src/game/m_item_name.c` | append `mIN_ARTICLE_A`/`AN` to `itemArt_Fish[]` |
| 14 | `src/data/model/inv_mwin3.c` | icon palette (reuse a similar fish's CI4 texture with a recolored 32-entry palette) |
| 15 | `src/game/m_submenu_ovl.c` | extern + append `{ pal, tex }` to `fish_tex_table[]` |
| 16 | `src/actor/ac_set_ovl_gyoei.c` | `FISH_SPAWN(NAME, AREA, weight)` in each month/time array **and bump the array size + `aSOG_term_list_c` count** |
| 17 | `src/game/m_inventory_ovl.c` | put `aGYO_TYPE_<NAME>` into a `mIV_fish_collect_list2[]` slot |
| 18 | `src/actor/npc/ac_npc_curator_move.c_inc` | append a message id to the donation `msg_no[]` |
| 19 | `fish/gen_fish_table.py` | add the display name to `DISPLAY_NAMES` |

Already handled generically (no per-fish change needed): catch flow & pocket
item, sell price at Nook's, encyclopedia caught-bit
(`mSM_COLLECT_FISH_GET/SET` stores modded bits in unused save space
`Private_c.unused_2412`, so vanilla saves stay compatible), release-into-water
remap, held-fish model remap, **house placement + tank rendering** (see below),
catch message (falls back to the generic "I caught something!" line — see
Limitations).

## House tank (fish furniture) - status: PARKED

Dropping a fish in your house converts it to furniture. Vanilla fish map to
`FTR_FISH_START + idx*4`, but that range is full (umbrellas follow it), so a
modded-fish tank needs new furniture kinds at the end of the FTR1 space.

A complete implementation exists but is currently **disabled** (the generated
fish model needs more art iteration):

* [src/furniture/ac_mod_fish_tank.c](../src/furniture/ac_mod_fish_tank.c) -
  shared tank profile + draw proc (kept in the tree, not compiled).
* To re-enable: re-add `X(FTR_MOD_FISH00)` before `FTR1_END`
  (include/m_name_table.h), `FTR_MOD_FISH00` before `FTR_NUM`
  (include/m_ftr_def.h), `&iam_mod_fish00` at the end of `furniture_quality[]`,
  the extern in include/f_furniture.h, the two `#include` lines in
  src/f_furniture.c, and restore the item<->ftr remaps in
  src/game/m_room_type.c (git history has all of these).
* Until then, [m_room_type.c](../src/game/m_room_type.c) explicitly makes
  modded fish **non-placeable** - do not remove that guard: without it the
  vanilla conversion maps fish idx 40 into the umbrella furniture range.

## Generating a fish model (`fish/gen_fish_model.py`)

Each fish's 3D model (used when swimming after release, held overhead, and in
the house tank) is generated — no art tools needed:

```bash
python fish/gen_fish_model.py --list     # available specs
python fish/gen_fish_model.py tetra      # writes src/data/model/act_f41_tetra.c
```

A spec defines length/height and palette roles (back, belly, lateral stripe,
rear/tail, outline, eye). The script paints a 32x32 CI4 texture (GameCube
8x8-block swizzled), builds a matching low-poly double-sided side-profile mesh
with UVs derived from the same outline function, and emits three vertex frames
(tail bent up / neutral / down) with display lists identical in style to the
vanilla `act_f##` models. It prints the registration snippet for
`ac_gyoei_model.c_inc` and the `#include` line for `src/f_furniture.c`.

**Status:** the generated tetra model is currently *not wired in* (needs art
iteration); the tetra uses the vanilla guppy model. To swap the generated one
back in: `#include "../src/data/model/act_f41_tetra.c"` in src/f_furniture.c
and point the tetra's `aGYO_displayList` entry at an `aGYO_tetra_dl` built
from the `act_f41_tetra_*T_model` display lists.

**Icon palette rule:** entries 1 and 17 of the `inv_mwin_*` icon palettes are
the shared dark-blue background disc behind every item icon - never recolor
them (keep `0xB19F` / `0xA66D`), or the item's background won't match the rest
of the inventory.

## Known limitations (v1)

* **Catch message**: modded fish use the generic fallback message (`0x10F2`),
  since fish-specific catchphrases live in `forest_2nd.arc`. You can hijack an
  existing message via `dialog/dialog.json` + `aTRC_clip_get_msgno()` if desired.

## Completion requirements (implemented)

* **Golden rod**: awarded via `mSM_CHECK_ALL_FISH_GET()` which compares against
  `FISH_NUM` using `mSM_COLLECT_FISH_GET` — modded fish are REQUIRED and the
  requirement scales automatically as `FISH_NUM` grows.
* **Museum**: modded fish are **not donatable and are not required** for museum
  fish-wing completion. If the player tries to donate one, Blathers returns it
  with a custom message pointing them to Porter at the train station.

## Step 1 — Fish type enum (`include/ac_gyoei.h`)

The vanilla layout is tightly packed:

```
0..39  real fish            (aGYO_TYPE_NUM == 40)
40     whale (event only)
41..43 trash (can/boot/tire)
44     salmon2 (river-mouth salmon variant)   (aGYO_TYPE_EXTENDED_NUM == 45)
```

New fish must be appended **after** `aGYO_TYPE_EXTENDED_NUM` (values 45+), e.g.
`aGYO_TYPE_TUNA = 45`, and a new terminator (e.g. `aGYO_TYPE_MODDED_NUM`)
added. Do **not** insert before index 40 — the 0–39 range is baked into save
data (collected bitfield), item IDs, price and message tables.

Every table indexed by fish type must be extended to the new count:

- `gyoei_type[]` in `src/actor/ac_gyoei_type.c_inc` — add `{ size, search_area, bite_time }`
  (`search_area`: 1–4, radius the fish notices the bobber; `bite_time`: 0–4 fake-bite count, 0 = bites instantly).
- `aUKI_get_fish_type()`'s `fish_data[]` in `src/actor/ac_uki_move.c_inc` — maps
  `gyo_type` → item number (see step 2). The bounds check uses
  `aGYO_TYPE_EXTENDED_NUM`; update it to the new terminator.
- The gyoei (shadow) actor draw tables in `src/actor/ac_gyoei_draw.c_inc` /
  model data — the swimming shadow is generic per size, so usually no change.

## Step 2 — Item number (`include/m_name_table.h`)

Fish items live at `ITM_FISH_START` (`0x2300`) + fish index; the item number
encodes `NAME_TYPE_ITEM1` (nibble `0x2`) + `ITEM1_CAT_FISH` (nibble `0x3`) +
index byte. `ITM_FISH_END` is `0x2300 + 40` and the low byte has room up to
`0x23FF`, so:

- Add `#define ITM_FISH40 (ITM_FISH_START + 40)` … etc. for each new fish.
  **Caution:** index 40–44 in `aUKI_get_fish_type()`'s `fish_data[]` are
  whale/trash/salmon2 — the *item* index and the *gyo_type* index diverge past
  39. Give the new fish item index = its encyclopedia identity (40, 41, …) and
  map its gyo_type (45, 46, …) to that item in `fish_data[]`.
- Update `ITM_FISH_END` and everything that uses it
  (`ITEM_IS_FISH`, loops in shops/museum — grep `ITM_FISH_END`).
- `mNT_FishIdx2FishItemNo()` converts fish index → item number; verify it is a
  simple `ITM_FISH_START + idx` for indexes ≥ 40.

## Step 3 — Price (`src/data/item/fish_price.c`)

Append the **catalog** price before the `-1` terminator. The player receives
`catalog / 4` when selling (`SELL_BUY_RATIO == 4`,
`src/actor/npc/ac_npc_shop_common.c`). Selling "just works" once the item is a
valid `ITEM1_CAT_FISH` item with a price entry — `mSP_ItemNo2ItemPrice()`
indexes this table by `item_no - ITM_FISH_START`.

## Step 4 — Name, icon, model, description

Binary assets — all indexed by fish/item index:

| Asset | Location | Notes |
|---|---|---|
| Item name | `assets/itemName_fish.inc` (built into `itemName_fish[]`, `src/data/item/item_name.c`) | fixed-width name records; append one record per fish |
| Menu icon | inventory icon sheet (`inv_mwin_*_tex` assets) | 16×16 icon per fish, referenced by item draw code |
| Held/menu model | `act_f##_*` model + texture assets | copy an existing fish model as a starting point |
| Catch message | message table in `src/actor/ac_turi_clip.c_inc` (`0x10F6 + idx`) | "I caught a …!" text lives in the message data files |
| Museum donation | N/A | modded fish are refused by Blathers |

These are the most labor-intensive steps because they are binary/asset edits,
not C tables. Use the existing extraction/build pipeline (`configure.py`,
`assets/`) and crib from a similar-sized vanilla fish.

## Step 5 — Spawn tables (`src/actor/ac_set_ovl_gyoei.c`)

This is what makes the fish appear in the world with correct
month/time/weather behavior:

1. For each month/half-month the fish should spawn in, add a
   `FISH_SPAWN(NAME, AREA, weight)` entry to the relevant
   `aSOG_term_info_c` array (`r_*` = river/pool/waterfall, `s_*` = sea,
   `p_*` = pond) **and bump the array's declared size and the count in the
   matching `aSOG_term_list_c`**. Weights are relative within the list
   (bigger = more common; vanilla uses 1–40).
2. Time-of-day = which of the four slots of the `*_month` term list you edit.
3. Weather-conditional spawns follow the coelacanth pattern:
   `aSOG_add_kaseki_range_data()` appends a spawn entry at runtime when
   `mEnv_NowWeather() == mEnv_WEATHER_RAIN`. Copy that function for custom
   conditions (snow, evening only, etc.).
4. Island spawns: `f_il_t*` / `f_island`; fishing tourney: `f_bs_t*` / `f_event`.

Shadow size, bite behavior, and catch flow (bobber → hook → item into pockets
→ `mFR` record → collected bit) all key off the tables from steps 1–2
automatically — no extra code needed.

## Step 6 — Encyclopedia slot (`src/game/m_inventory_ovl.c`)

Add the fish to page 2 by replacing an `E` (= `mIV_FISH_SLOT_EMPTY`) in
`mIV_fish_collect_list2[]` with `F(NAME)` (move the `#define F` up to cover
both lists, or write `aGYO_TYPE_NAME` directly). Slots fill left→right,
top→bottom, matching page 1's 8×5 layout.

**Collected bit:** `mIV_set_collect_itemNo()` checks
`Now_Private->furniture_collected_bitfield` at
`FTR_NO_2_IDX(FTR_SUM_FUNA) + fish_idx`. Vanilla reserves bits for the 40
fish; new fish (idx ≥ 40) need bits allocated after the vanilla insect range —
audit `include/m_private.h` (`furniture_collected_bitfield` size) and
`mPr_SetItemCollectBit()` to confirm free space before shipping. The fish page-2
code returns "not caught" for any slot whose lookup would go out of range.

## Step 7 — Regenerate docs and build

```bash
python fish/gen_fish_table.py --write   # refresh fish/fish.md from source
ninja                                    # build (sha1 CHECK failure is expected)
```

Smoke test in Dolphin:

1. Open the menu -> click the fish tab -> page 1 shows as usual.
2. After at least one page-2 fish is registered, use the bottom-center right
   arrow to open page 2, then the left arrow to return to page 1. The disabled
   arrow should stay visible but should not change pages.
3. Catch the new fish at the right place/time; confirm the catch message,
   pocket icon, sell price at Nook's, and that its encyclopedia circle fills in.

---

## Encyclopedia paging - how it works (implemented)

- `mIV_Ovl_c.fish_page_no` (new field, `include/m_inventory_ovl.h`) selects the
  active fish sub-page; `mIV_FISH_PAGE_NUM` is the page count (currently 2).
- The fish tab only changes to the fish encyclopedia. Page changes happen
  through `mTG_TABLE_FISH_PAGE_ARROW` at the bottom center of the fish page.
- The arrows are drawn only when `mIV_has_registered_mod_fish()` finds a
  collected page-2 fish. Both arrows stay visible then, but
  `mIV_can_change_fish_page()` controls which one is clickable for the current
  page.
- `mIV_set_collect_itemNo` reads `mIV_fish_collect_list2[]` when
  `fish_page_no != 0`.
- To add a third page: bump `mIV_FISH_PAGE_NUM`, add `mIV_fish_collect_list3[]`,
  extend the list selection in `mIV_set_collect_itemNo`, and teach
  `mIV_can_change_fish_page()` about the new upper bound.
