#!/usr/bin/env python3
"""gen_fish_table.py — Generate/verify fish/fish.md from the actual game code.

Parses the real data tables in the decomp so the markdown table can never
drift from the game:

  * src/actor/ac_gyoei_type.c_inc      -> shadow sizes (aGYO_SIZE_*)
  * src/data/item/fish_price.c         -> prices (sell price = catalog / 4)
  * src/actor/ac_set_ovl_gyoei.c       -> spawn months / time slots / areas
  * src/game/m_inventory_ovl.c         -> encyclopedia display order (both pages)
  * include/ac_gyoei.h                 -> fish type enum order

Usage (from repo root):
    python fish/gen_fish_table.py            # print the table
    python fish/gen_fish_table.py --write    # rewrite fish/fish.md

Re-run with --write any time fish data or new fish are added.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

GYOEI_H = REPO / "include" / "ac_gyoei.h"
TYPE_INC = REPO / "src" / "actor" / "ac_gyoei_type.c_inc"
PRICE_C = REPO / "src" / "data" / "item" / "fish_price.c"
SPAWN_C = REPO / "src" / "actor" / "ac_set_ovl_gyoei.c"
INV_C = REPO / "src" / "game" / "m_inventory_ovl.c"
FISH_MD = REPO / "fish" / "fish.md"

# Display names, indexed by aGYO_TYPE_* enum name.
DISPLAY_NAMES = {
    "CRUCIAN_CARP": "Crucian carp", "BROOK_TROUT": "Brook trout", "CARP": "Carp",
    "KOI": "Koi", "CATFISH": "Catfish", "SMALL_BASS": "Small bass", "BASS": "Bass",
    "LARGE_BASS": "Large bass", "BLUEGILL": "Bluegill", "GIANT_CATFISH": "Giant catfish",
    "GIANT_SNAKEHEAD": "Giant snakehead", "BARBEL_STEED": "Barbel steed", "DACE": "Dace",
    "PALE_CHUB": "Pale chub", "BITTERLING": "Bitterling", "LOACH": "Loach",
    "POND_SMELT": "Pond smelt", "SWEETFISH": "Sweetfish", "CHERRY_SALMON": "Cherry salmon",
    "LARGE_CHAR": "Large char", "RAINBOW_TROUT": "Rainbow trout", "STRINGFISH": "Stringfish",
    "SALMON": "Salmon", "GOLDFISH": "Goldfish", "PIRANHA": "Piranha", "AROWANA": "Arowana",
    "EEL": "Eel", "FRESHWATER_GOBY": "Freshwater goby", "ANGELFISH": "Angelfish",
    "GUPPY": "Guppy", "POPEYED_GOLDFISH": "Popeyed goldfish", "COELACANTH": "Coelacanth",
    "CRAWFISH": "Crawfish", "FROG": "Frog", "KILLIFISH": "Killifish",
    "JELLYFISH": "Jellyfish", "SEA_BASS": "Sea bass", "RED_SNAPPER": "Red snapper",
    "BARRED_KNIFEJAW": "Barred knifejaw", "ARAPAIMA": "Arapaima",
    # modded fish
    "NEON_TETRA": "Neon tetra",
}

SIZE_NAMES = {
    "aGYO_SIZE_XXS": "Tiny (XXS)", "aGYO_SIZE_XS": "Small (XS)", "aGYO_SIZE_S": "Small-Med (S)",
    "aGYO_SIZE_M": "Medium (M)", "aGYO_SIZE_L": "Large (L)", "aGYO_SIZE_XL": "Very Large (XL)",
    "aGYO_SIZE_XXL": "Huge (XXL)", "aGYO_SIZE_WHALE": "Whale",
}

AREA_NAMES = {
    "POOL": "River (pool)", "WATERFALL": "Waterfall", "RIVER_MOUTH": "River (mouth)",
    "OFFING": "Sea (deep)", "SEA": "Sea", "RIVER": "River", "POND": "Pond",
}

# Time slot index -> (start hour, end hour) in 24h, end exclusive. Slot 0 wraps midnight.
# From aSOG_TIME_NO_*_END: 0 = 9pm-3:59am, 1 = 4am-8:59am, 2 = 9am-3:59pm, 3 = 4pm-8:59pm
SLOT_HOURS = {0: (21, 28), 1: (4, 9), 2: (9, 16), 3: (16, 21)}

MONTH_LETTERS = "JFMAMJJASOND"


def die(msg: str):
    sys.exit(f"gen_fish_table: ERROR: {msg}")


def parse_enum_order() -> list[str]:
    """aGYO_TYPE_* names indexed by enum value (first 40 = real fish)."""
    text = GYOEI_H.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"enum\s+fish_type\s*\{(.*?)\};", text, re.S)
    if not m:
        die(f"fish_type enum not found in {GYOEI_H}")
    body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
    body = re.sub(r"//[^\n]*", "", body)
    values: dict[str, int] = {}
    order: dict[int, str] = {}
    next_val = 0
    for entry in body.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if "=" in entry:
            name, rhs = (s.strip() for s in entry.split("=", 1))
            next_val = int(rhs) if rhs.isdigit() else values[rhs]
        else:
            name = entry
        values[name] = next_val
        if not name.endswith("_NUM"):
            order.setdefault(next_val, name.replace("aGYO_TYPE_", ""))
        next_val += 1
    return [order.get(i, f"?{i}") for i in range(max(order) + 1)]


def parse_sizes() -> list[str]:
    """aGYO_SIZE_* per fish, in enum order."""
    text = TYPE_INC.read_text(encoding="utf-8", errors="replace")
    return re.findall(r"\{\s*(aGYO_SIZE_\w+)\s*,", text)


def parse_prices() -> list[int]:
    text = PRICE_C.read_text(encoding="utf-8", errors="replace")
    body = re.search(r"fish_price_table\[\]\s*=\s*\{(.*?)\};", text, re.S)
    if not body:
        die(f"fish_price_table not found in {PRICE_C}")
    vals = [int(v) for v in re.findall(r"(-?\d+)", body.group(1))]
    if vals and vals[-1] == -1:
        vals = vals[:-1]  # end marker
    return vals


def parse_spawns():
    """Return {fish_enum: {"months": set(1..12), "slots": set(0..3), "areas": set(str)}}."""
    text = SPAWN_C.read_text(encoding="utf-8", errors="replace")

    # 1. term info arrays: name -> [(fish, area), ...]
    infos: dict[str, list[tuple[str, str]]] = {}
    for m in re.finditer(r"static\s+aSOG_term_info_c\s+(\w+)\[\d*\]\s*=\s*\{(.*?)\};", text, re.S):
        entries = re.findall(r"FISH_SPAWN\(\s*(\w+)\s*,\s*(\w+)\s*,", m.group(2))
        infos[m.group(1)] = entries

    # 2. term lists (4 time slots): name -> [info_name x4]
    lists: dict[str, list[str]] = {}
    for m in re.finditer(r"static\s+aSOG_term_list_c\s+(\w+)\[aSOG_TIME_NUM\]\s*=\s*\{(.*?)\};", text, re.S):
        slots = re.findall(r"\{\s*\d+\s*,\s*(\w+)\s*\}", m.group(2))
        lists[m.group(1)] = slots

    # 3. month tables: r_month / s_month / p_month -> [12][2] of list name or NULL
    month_tables: dict[str, list[tuple[str, str]]] = {}
    for m in re.finditer(r"static\s+aSOG_term_list_c\*\s+(\w+)\[lbRTC_MONTHS_MAX\]\[aSOG_TERM_NUM\]\s*=\s*\{(.*?)\};",
                         text, re.S):
        rows = re.findall(r"\{\s*(\w+)\s*,\s*(\w+)\s*\}", m.group(2))
        month_tables[m.group(1)] = rows

    for req in ("r_month", "s_month", "p_month"):
        if req not in month_tables or len(month_tables[req]) != 12:
            die(f"{req} table missing/malformed in {SPAWN_C}")

    fish: dict[str, dict] = {}

    def add(enum_name: str, area: str, month: int | None, slot: int):
        # SALMON2 is the river-mouth variant of SALMON (same item)
        key = "SALMON" if enum_name == "SALMON2" else enum_name
        f = fish.setdefault(key, {"months": set(), "slots": set(), "areas": set()})
        if month is not None:
            f["months"].add(month)
        f["slots"].add(slot)
        f["areas"].add(area)

    for table in ("r_month", "s_month", "p_month"):
        for month_idx, (first, second) in enumerate(month_tables[table], start=1):
            for list_name in (first, second):
                if list_name == "NULL":
                    continue
                for slot, info_name in enumerate(lists[list_name]):
                    for enum_name, area in infos[info_name]:
                        add(enum_name, area, month_idx, slot)

    # Coelacanth: added dynamically (aSOG_add_kaseki_range_data) — sea, raining,
    # any month, all slots except 2 (9am-4pm).
    m = re.search(r"aSOG_add_kaseki_range_data.*?FISH_SPAWN\(\s*(\w+)\s*,\s*(\w+)\s*,", text, re.S)
    if m:
        enum_name, area = m.group(1), m.group(2)
        for month in range(1, 13):
            for slot in (0, 1, 3):
                add(enum_name, area, month, slot)
        fish[enum_name]["rain_only"] = True

    # Island / fishing tourney extras (availability notes only)
    for special, note in (("f_island", "island"), ("f_event", "tourney")):
        if special in lists:
            for info_name in lists[special]:
                for enum_name, _area in infos[info_name]:
                    key = "SALMON" if enum_name == "SALMON2" else enum_name
                    fish.setdefault(key, {"months": set(), "slots": set(), "areas": set()})
                    fish[key].setdefault("notes", set()).add(note)

    return fish


def parse_collect_lists() -> tuple[list[str], list[str]]:
    """Encyclopedia display order for page 1 (and page 2 if present)."""
    text = INV_C.read_text(encoding="utf-8", errors="replace")

    def grab(name: str) -> list[str]:
        m = re.search(rf"static\s+u8\s+{name}\[[^\]]*\]\s*=\s*\{{(.*?)\}};", text, re.S)
        if not m:
            return []
        body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        out = []
        for tok in re.split(r"[,\s]+", body):
            if not tok:
                continue
            if tok in ("E", "mIV_FISH_SLOT_EMPTY"):
                out.append("mIV_FISH_SLOT_EMPTY")
            elif tok.startswith("F(") and tok.endswith(")"):
                out.append(tok[2:-1])
            elif tok.startswith("aGYO_TYPE_"):
                out.append(tok[len("aGYO_TYPE_"):])
        return out

    return grab("mIV_fish_collect_list"), grab("mIV_fish_collect_list2")


def slots_to_time_str(slots: set[int]) -> str:
    if slots >= {0, 1, 2, 3}:
        return "All day"
    # Convert slots to hour intervals on a 4am-based ring, then merge.
    ivals = sorted((SLOT_HOURS[s][0] % 24, SLOT_HOURS[s][1]) for s in slots)
    # normalize to ring starting at 4am
    ring = sorted(((s - 4) % 24, (e - 4 - 1) % 24 + 1) for s, e in ivals)
    merged: list[list[int]] = []
    for s, e in ring:
        if merged and merged[-1][1] == s:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    # wrap-around join
    if len(merged) > 1 and merged[0][0] == 0 and merged[-1][1] == 24:
        merged[0][0] = merged[-1][0] - 24
        merged.pop()

    def hr(h):
        h %= 24
        if h == 0:
            return "midnight"
        if h == 12:
            return "noon"
        return f"{h % 12 or 12} {'AM' if h < 12 else 'PM'}"

    return "; ".join(f"{hr(s + 4)} \u2013 {hr(e + 4)}" for s, e in merged)


def months_to_str(months: set[int]) -> str:
    return "".join(MONTH_LETTERS[i - 1] if i in months else "\u2013" for i in range(1, 13))


def build_rows():
    enum_order = parse_enum_order()
    sizes = parse_sizes()
    prices = parse_prices()
    spawns = parse_spawns()
    page1, page2 = parse_collect_lists()

    n_fish = 40
    if len(prices) < n_fish:
        die(f"expected at least {n_fish} prices, found {len(prices)}")
    if len(sizes) < n_fish:
        die(f"expected at least {n_fish} size entries, found {len(sizes)}")
    if len(page1) != n_fish:
        die(f"expected 40 entries in mIV_fish_collect_list, found {len(page1)}")

    idx_of = {name: i for i, name in enumerate(enum_order)}
    # vanilla enum: 0-39 fish, 40-44 whale/trash/salmon2, 45+ modded fish.
    # fish/item index: 0-39 vanilla, 40+ modded (skips the whale/trash block).
    VANILLA_FISH = 40
    EXTENDED = 45

    def fish_index(enum_idx: int) -> int:
        return enum_idx if enum_idx < VANILLA_FISH else VANILLA_FISH + (enum_idx - EXTENDED)

    def make_row(pos: int, enum_name: str):
        i = idx_of[enum_name]
        fi = fish_index(i)
        sp = spawns.get(enum_name, {"months": set(), "slots": set(), "areas": set()})
        areas = ", ".join(sorted(AREA_NAMES[a] for a in sp["areas"])) or "\u2014"
        if sp.get("rain_only"):
            areas += " (raining)"
        time_str = slots_to_time_str(sp["slots"]) if sp["slots"] else "\u2014"
        notes = ", ".join(sorted(sp.get("notes", set())))
        if i >= EXTENDED:
            notes = ("modded, " + notes) if notes else "modded"
        sell = prices[fi] // 4
        return (f"| {pos} | {DISPLAY_NAMES[enum_name]} | {sell:,} Bells | "
                f"{SIZE_NAMES[sizes[i]]} | {areas} | {time_str} | "
                f"{months_to_str(sp['months'])} | {notes} |")

    header = ("| # | Name | Sell price | Shadow size | Location | Time | Months | Notes |\n"
              "|---|------|-----------|-------------|----------|------|--------|-------|")
    rows1 = [make_row(pos + 1, e) for pos, e in enumerate(page1)]

    rows2 = []
    for pos, e in enumerate(page2):
        if e == "mIV_FISH_SLOT_EMPTY":
            rows2.append(f"| {pos + 41} | *(empty slot)* | \u2014 | \u2014 | \u2014 | \u2014 | \u2013\u2013\u2013\u2013\u2013\u2013\u2013\u2013\u2013\u2013\u2013\u2013 | |")
        else:
            rows2.append(make_row(pos + 41, e))

    return header, rows1, rows2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="rewrite fish/fish.md")
    args = ap.parse_args()

    header, rows1, rows2 = build_rows()

    out = ["# Fish (generated from game code — do not hand-edit)",
           "",
           "Regenerate with: `python fish/gen_fish_table.py --write`",
           "",
           "Sources: `src/actor/ac_set_ovl_gyoei.c` (spawns), `src/data/item/fish_price.c`",
           "(sell = catalog price / 4), `src/actor/ac_gyoei_type.c_inc` (shadow sizes),",
           "`src/game/m_inventory_ovl.c` (encyclopedia order).",
           "",
           "Time slots are the game's four spawn windows: 9 PM\u20134 AM, 4\u20139 AM, 9 AM\u20134 PM, 4\u20139 PM.",
           "Months: letter = available that month (spawn tables are per half-month; both halves merged).",
           "Notes: `island` = also spawns at the island, `tourney` = boosted during the fishing tourney.",
           "",
           "## Page 1",
           "",
           header]
    out += rows1
    if rows2:
        out += ["", "## Page 2 (new fish)", "", header]
        out += rows2
    text = "\n".join(out) + "\n"

    if args.write:
        FISH_MD.write_text(text, encoding="utf-8")
        print(f"wrote {FISH_MD}")
    else:
        print(text)


if __name__ == "__main__":
    main()
