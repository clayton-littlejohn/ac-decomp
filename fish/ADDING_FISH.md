# Adding a New Fish — Complete Workflow

This document is the checklist for adding a brand-new, fully functional fish to
Animal Crossing (GameCube). Follow it top to bottom; every step maps to a real
table in the decompiled source. After each addition, run
`python fish/gen_fish_table.py --write` to regenerate [fish.md](fish.md) and confirm
the game data matches your intent, then build with `ninja` (the
`CHECK build.sha1` step will report FAILED — that is expected for a mod).

The engine identifies a fish by its **`aGYO_TYPE_*` index**. Every table below
is indexed by (or maps to) that number, so all steps must stay in the same
order.

---

## Step 0 — Pick the fish's identity

Decide up front:

| Property | Where it lives | Example |
|---|---|---|
| Enum name | `include/ac_gyoei.h` | `aGYO_TYPE_TUNA` |
| Shadow size | `src/actor/ac_gyoei_type.c_inc` | `aGYO_SIZE_XL` |
| Sell price | `src/data/item/fish_price.c` | catalog `8000` → sells for 2,000 Bells |
| Spawn area(s) | `src/actor/ac_set_ovl_gyoei.c` | `SEA`, `RIVER`, `POOL`, `POND`, `WATERFALL`, `RIVER_MOUTH`, `OFFING` |
| Months + time slots | same file | e.g. Dec–Feb, slots 0/1/3 (4 PM–9 AM) |
| Encyclopedia slot | `src/game/m_inventory_ovl.c` (`mIV_fish_collect_list2`) | page 2, slot 1 |

Time slots (per day): `0` = 9 PM–4 AM, `1` = 4–9 AM, `2` = 9 AM–4 PM, `3` = 4–9 PM.
Spawn tables are per **half-month** (`aSOG_TERM_0`/`aSOG_TERM_1`), so seasonal
boundaries can land mid-month.

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
| Museum donation | `src/data/scene/museum_fish.c` + curator dialog | optional but needed for donations |

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

1. Open the menu → click the fish tab → page 1 shows as usual.
2. Click the fish tab again → window plays the tab transition and shows page 2.
3. Catch the new fish at the right place/time; confirm the catch message,
   pocket icon, sell price at Nook's, and that its encyclopedia circle fills in.

---

## Encyclopedia paging — how it works (implemented)

- `mIV_Ovl_c.fish_page_no` (new field, `include/m_inventory_ovl.h`) selects the
  active fish sub-page; `mIV_FISH_PAGE_NUM` is the page count (currently 2).
- Clicking the fish tab while the fish page is already in front
  (`mTG_select_tag_decide_wchange`, `src/game/m_tag_ovl.c`) starts the standard
  40-frame page transition targeting the fish page itself.
- `mIV_move_Play` (`src/game/m_inventory_ovl.c`) detects this "same-tab"
  transition at the midpoint (timer == 20) and advances
  `fish_page_no = (fish_page_no + 1) % mIV_FISH_PAGE_NUM` instead of reordering
  `page_order[]`; `mIV_up_page_draw_check` keeps only the fish window animating.
- `mIV_set_collect_itemNo` reads `mIV_fish_collect_list2[]` when
  `fish_page_no != 0`.
- To add a third page: bump `mIV_FISH_PAGE_NUM`, add `mIV_fish_collect_list3[]`,
  and extend the list selection in `mIV_set_collect_itemNo` — the transition
  logic already cycles through any number of pages.
