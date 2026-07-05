#!/usr/bin/env python3
"""add_fish.py — add modded fish to the game from the declarative specs below.

For every fish in FISH_SPECS that is not yet in the codebase, this script
patches ALL required touchpoints (see fish/ADDING_FISH.md):

  * include/ac_gyoei.h                enum aGYO_TYPE_*
  * src/actor/ac_gyoei_type.c_inc     shadow size / search area / bite time
  * src/actor/ac_gyoei_model.c_inc    swim model (reuses a vanilla aGYO_*_dl)
  * src/actor/ac_uki_move.c_inc       gyo type -> item mapping
  * src/actor/ac_gyo_release.c        release animation pattern
  * include/m_name_table.h            FISH_NUM
  * src/data/item/fish_price.c        catalog price (sell = /4)
  * src/data/item/item_name.c         16-byte item name
  * src/game/m_item_name.c            article (a/an)
  * src/data/model/inv_mwin_modfish_pal.c_inc   generated icon palettes
  * src/game/m_submenu_ovl.c          icon externs + fish_tex_table entries
  * src/actor/ac_set_ovl_gyoei.c      spawn tables (arrays + counts fixed up)
  * src/game/m_inventory_ovl.c        encyclopedia page-2 slots
  * fish/gen_fish_table.py            display names

Idempotent: fish whose enum already exists are skipped; the icon palette file
and the encyclopedia list are regenerated wholesale. Afterwards run:

    python fish/gen_fish_table.py --write
    python fish/make_iso.py
"""
from __future__ import annotations

import colorsys
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
INC = REPO / "include"

# ---------------------------------------------------------------------------
# Specs. Fields:
#   enum       aGYO_TYPE_<enum>
#   name       item name, lowercase, max 16 chars
#   display    encyclopedia display name
#   article    "A" or "AN"
#   price      catalog price (sell = price/4), u16
#   size       aGYO_SIZE_XXS..XXL   search 1-4   bite 0-4
#   anime      release animation: 1 = quick wiggle, 2 = slow
#   model      vanilla swim model to reuse (aGYO_<model>_dl)
#   icon       (vanilla fish idx 0-39 to borrow the icon texture from,
#               hue shift degrees, saturation mult, value mult)
#   area       spawn area: RIVER POOL WATERFALL RIVER_MOUTH SEA POND
#   months     list of month numbers (pond fish: only Apr-Sep have tables)
#   slots      time slots: 0=9pm-4am 1=4-9am 2=9am-4pm 3=4-9pm
#   weight     spawn weight (1-40, higher = more common)
# ---------------------------------------------------------------------------
ALL_YEAR = list(range(1, 13))
SUMMER = [6, 7, 8, 9]
WARM = [4, 5, 6, 7, 8, 9, 10]
WINTER = [12, 1, 2]
ALL_DAY = [0, 1, 2, 3]
NIGHT = [0, 3]
DAY = [1, 2]

F = dict  # noqa: E741 - terseness for the table below

FISH_SPECS = [
    # --- freshwater ---------------------------------------------------------
    F(enum="PIKE", name="pike", display="Pike", article="A", price=7200,
      size="L", search=2, bite=2, anime=2, model="raigyo", icon=(10, 100, 1.0, 1.05),
      area="RIVER", months=[9, 10, 11, 12], slots=ALL_DAY, weight=4),
    F(enum="YELLOW_PERCH", name="yellow perch", display="Yellow perch", article="A", price=1200,
      size="M", search=3, bite=3, anime=1, model="ugui", icon=(8, 45, 1.3, 1.1),
      area="RIVER", months=[10, 11, 12, 1, 2, 3], slots=ALL_DAY, weight=8),
    F(enum="STURGEON", name="sturgeon", display="Sturgeon", article="A", price=40000,
      size="XL", search=2, bite=1, anime=2, model="ito", icon=(21, -30, 0.7, 0.95),
      area="RIVER_MOUTH", months=[9, 10, 11, 12, 1, 2, 3], slots=ALL_DAY, weight=2),
    F(enum="GOLDEN_TROUT", name="golden trout", display="Golden trout", article="A", price=60000,
      size="M", search=1, bite=1, anime=1, model="niji", icon=(20, 60, 1.4, 1.15),
      area="WATERFALL", months=[3, 4, 5, 9, 10, 11], slots=[1, 3], weight=1),
    F(enum="TILAPIA", name="tilapia", display="Tilapia", article="A", price=3200,
      size="M", search=3, bite=3, anime=1, model="nigoi", icon=(11, 160, 1.1, 1.0),
      area="RIVER", months=SUMMER, slots=ALL_DAY, weight=6),
    F(enum="BETTA", name="betta", display="Betta", article="A", price=10000,
      size="XS", search=2, bite=2, anime=1, model="angel", icon=(28, 130, 1.4, 1.0),
      area="RIVER", months=[5, 6, 7, 8, 9, 10], slots=DAY, weight=2),
    F(enum="RAINBOWFISH", name="rainbowfish", display="Rainbowfish", article="A", price=3200,
      size="XXS", search=2, bite=2, anime=1, model="gupi", icon=(29, -160, 1.4, 1.1),
      area="RIVER", months=[5, 6, 7, 8, 9, 10], slots=DAY, weight=4),
    F(enum="GAR", name="gar", display="Gar", article="A", price=24000,
      size="XL", search=2, bite=1, anime=2, model="sake", icon=(22, 90, 1.1, 0.9),
      area="POND", months=SUMMER, slots=NIGHT, weight=2),
    F(enum="DORADO", name="dorado", display="Dorado", article="A", price=60000,
      size="L", search=1, bite=0, anime=1, model="aroana", icon=(25, 25, 1.4, 1.2),
      area="RIVER", months=[6, 7, 8, 9], slots=[1, 2], weight=1),
    F(enum="SADDLED_BICHIR", name="saddled bichir", display="Saddled bichir", article="A", price=16000,
      size="M", search=2, bite=2, anime=2, model="namazu", icon=(4, -50, 1.2, 1.0),
      area="RIVER", months=[6, 7, 8, 9], slots=NIGHT, weight=2),
    F(enum="NIBBLE_FISH", name="nibble fish", display="Nibble fish", article="A", price=6000,
      size="XXS", search=3, bite=2, anime=1, model="tanago", icon=(14, 150, 1.2, 1.05),
      area="RIVER", months=[5, 6, 7, 8, 9], slots=DAY, weight=3),
    F(enum="TADPOLE", name="tadpole", display="Tadpole", article="A", price=400,
      size="XXS", search=4, bite=4, anime=1, model="medaka", icon=(33, 0, 0.4, 0.6),
      area="POND", months=[4, 5, 6, 7], slots=ALL_DAY, weight=12),
    F(enum="SNAPPING_TURTLE", name="snapping turtle", display="Snapping turtle", article="A", price=20000,
      size="XL", search=2, bite=2, anime=2, model="kaseki", icon=(31, 110, 1.1, 0.9),
      area="RIVER", months=[8, 9], slots=[0], weight=2),
    F(enum="SOFTSHELL_TURTLE", name="softshell turtle", display="Softshell turtle", article="A", price=15000,
      size="L", search=2, bite=2, anime=2, model="kaseki", icon=(31, 60, 1.2, 1.0),
      area="RIVER", months=[8, 9], slots=[1, 3], weight=3),
    F(enum="MITTEN_CRAB", name="mitten crab", display="Mitten crab", article="A", price=8000,
      size="XS", search=3, bite=3, anime=1, model="zarigani", icon=(32, -25, 1.2, 0.9),
      area="RIVER", months=[9, 10, 11], slots=NIGHT, weight=4),
    # --- ocean --------------------------------------------------------------
    F(enum="TUNA", name="tuna", display="Tuna", article="A", price=28000,
      size="XL", search=2, bite=1, anime=2, model="suzuki", icon=(36, -25, 1.2, 1.1),
      area="SEA", months=[11, 12, 1, 2, 3, 4], slots=ALL_DAY, weight=2),
    F(enum="BLUE_MARLIN", name="blue marlin", display="Blue marlin", article="A", price=40000,
      size="XL", search=1, bite=1, anime=2, model="suzuki", icon=(36, -60, 1.5, 1.0),
      area="SEA", months=[11, 12, 1, 2, 3, 4, 7, 8, 9], slots=ALL_DAY, weight=1),
    F(enum="OCEAN_SUNFISH", name="ocean sunfish", display="Ocean sunfish", article="AN", price=16000,
      size="XXL", search=2, bite=2, anime=2, model="tai", icon=(37, 170, 0.6, 1.1),
      area="SEA", months=[7, 8, 9], slots=[1, 2, 3], weight=2),
    F(enum="RAY", name="ray", display="Ray", article="A", price=12000,
      size="XL", search=2, bite=2, anime=2, model="isidai_alias_ishidai", icon=(38, 40, 0.8, 1.0),
      area="SEA", months=[8, 9, 10, 11], slots=[1, 2, 3], weight=3),
    F(enum="SAW_SHARK", name="saw shark", display="Saw shark", article="A", price=48000,
      size="XL", search=2, bite=1, anime=2, model="suzuki", icon=(36, 15, 0.5, 0.85),
      area="SEA", months=[6, 7, 8, 9], slots=NIGHT, weight=2),
    F(enum="HAMMERHEAD_SHARK", name="hammerhead shark", display="Hammerhead shark", article="A", price=32000,
      size="XL", search=2, bite=1, anime=2, model="suzuki", icon=(36, -10, 0.6, 0.75),
      area="SEA", months=[6, 7, 8, 9], slots=NIGHT, weight=2),
    F(enum="GREAT_WHITE_SHARK", name="gt. white shark", display="Great white shark", article="A", price=60000,
      size="XXL", search=1, bite=0, anime=2, model="piraluku", icon=(39, -20, 0.5, 1.0),
      area="SEA", months=[6, 7, 8, 9], slots=NIGHT, weight=1),
    F(enum="WHALE_SHARK", name="whale shark", display="Whale shark", article="A", price=52000,
      size="XXL", search=2, bite=1, anime=2, model="piraluku", icon=(39, -140, 0.9, 0.95),
      area="SEA", months=[6, 7, 8, 9], slots=ALL_DAY, weight=1),
    F(enum="NAPOLEONFISH", name="napoleonfish", display="Napoleonfish", article="A", price=40000,
      size="XXL", search=2, bite=1, anime=2, model="tai", icon=(37, -140, 1.2, 1.0),
      area="SEA", months=[7, 8], slots=[1, 2], weight=1),
    F(enum="BARRELEYE", name="barreleye", display="Barreleye", article="A", price=60000,
      size="XS", search=1, bite=1, anime=1, model="wakasagi", icon=(16, -140, 1.0, 0.8),
      area="SEA", months=ALL_YEAR, slots=[0], weight=1),
    F(enum="MAHI_MAHI", name="mahi-mahi", display="Mahi-mahi", article="A", price=24000,
      size="L", search=2, bite=2, anime=1, model="suzuki", icon=(36, 130, 1.4, 1.15),
      area="SEA", months=[5, 6, 7, 8, 9, 10], slots=[1, 2, 3], weight=2),
    F(enum="RIBBON_EEL", name="ribbon eel", display="Ribbon eel", article="A", price=2400,
      size="S", search=2, bite=2, anime=2, model="unagi", icon=(26, -150, 1.4, 1.1),
      area="SEA", months=[6, 7, 8, 9, 10], slots=ALL_DAY, weight=4),
    F(enum="MORAY_EEL", name="moray eel", display="Moray eel", article="A", price=8000,
      size="M", search=2, bite=2, anime=2, model="unagi", icon=(26, 60, 1.1, 0.9),
      area="SEA", months=[8, 9, 10], slots=ALL_DAY, weight=3),
    F(enum="SEAHORSE", name="seahorse", display="Seahorse", article="A", price=4400,
      size="XXS", search=3, bite=3, anime=1, model="tanago", icon=(14, 60, 1.3, 1.15),
      area="SEA", months=WARM, slots=ALL_DAY, weight=4),
    F(enum="CLOWNFISH", name="clownfish", display="Clownfish", article="A", price=2600,
      size="XXS", search=3, bite=3, anime=1, model="kingyo", icon=(23, 15, 1.4, 1.15),
      area="SEA", months=WARM, slots=DAY, weight=5),
    F(enum="SURGEONFISH", name="surgeonfish", display="Surgeonfish", article="A", price=4000,
      size="XS", search=3, bite=3, anime=1, model="gill_alias_blue_gill", icon=(8, -110, 1.5, 1.1),
      area="SEA", months=WARM, slots=DAY, weight=4),
    F(enum="BUTTERFLY_FISH", name="butterfly fish", display="Butterfly fish", article="A", price=4000,
      size="XS", search=3, bite=3, anime=1, model="demekin", icon=(30, 55, 1.4, 1.2),
      area="SEA", months=WARM, slots=DAY, weight=4),
    F(enum="ZEBRA_TURKEYFISH", name="zebra turkeyfish", display="Zebra turkeyfish", article="A", price=2000,
      size="S", search=2, bite=2, anime=2, model="donko", icon=(27, 20, 0.9, 1.15),
      area="SEA", months=WARM, slots=ALL_DAY, weight=3),
    F(enum="PUFFER_FISH", name="puffer fish", display="Puffer fish", article="A", price=1000,
      size="S", search=3, bite=3, anime=1, model="demekin", icon=(30, -35, 0.9, 1.1),
      area="SEA", months=[7, 8, 9], slots=ALL_DAY, weight=5),
    F(enum="HORSE_MACKEREL", name="horse mackerel", display="Horse mackerel", article="A", price=600,
      size="XS", search=4, bite=4, anime=1, model="oikawa", icon=(13, -40, 1.1, 1.1),
      area="SEA", months=ALL_YEAR, slots=ALL_DAY, weight=15),
    F(enum="SQUID", name="squid", display="Squid", article="A", price=2000,
      size="S", search=3, bite=3, anime=2, model="kurage", icon=(35, -20, 0.8, 1.15),
      area="SEA", months=[12, 1, 2, 3, 4, 5, 6, 7, 8], slots=ALL_DAY, weight=6),
    F(enum="ANCHOVY", name="anchovy", display="Anchovy", article="AN", price=800,
      size="XXS", search=4, bite=4, anime=1, model="wakasagi", icon=(16, -60, 1.2, 1.0),
      area="SEA", months=ALL_YEAR, slots=[1, 2], weight=12),
    F(enum="FOOTBALL_FISH", name="football fish", display="Football fish", article="A", price=10000,
      size="L", search=2, bite=1, anime=2, model="donko", icon=(27, -110, 0.9, 0.7),
      area="SEA", months=[11, 12, 1, 2, 3], slots=[0], weight=2),
    F(enum="OLIVE_FLOUNDER", name="olive flounder", display="Olive flounder", article="AN", price=3200,
      size="L", search=3, bite=3, anime=2, model="donko", icon=(27, 75, 0.9, 0.95),
      area="SEA", months=ALL_YEAR, slots=ALL_DAY, weight=6),
]

VANILLA_FISH = 40
BASE_GYO_TYPE = 45  # aGYO_TYPE_NEON_TETRA; new fish follow it
BASE_FISH_IDX = 41  # neon tetra is fish idx 40


def die(msg):
    sys.exit(f"add_fish: ERROR: {msg}")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, text: str):
    p.write_text(text, encoding="utf-8")
    print(f"  patched {p.relative_to(REPO)}")


def insert_after(text: str, anchor: str, addition: str, path: Path) -> str:
    idx = text.find(anchor)
    if idx < 0:
        die(f"anchor not found in {path}: {anchor[:60]!r}")
    end = idx + len(anchor)
    return text[:end] + addition + text[end:]


def model_dl(name: str) -> str:
    """Spec model field -> aGYO_*_dl symbol (handles alias syntax)."""
    if "_alias_" in name:
        name = name.split("_alias_")[1]
    return f"aGYO_{name}_dl"


# ---------------------------------------------------------------------------
def main():
    gyoei_h = INC / "ac_gyoei.h"
    text = read(gyoei_h)

    # deterministic indices: FISH_SPECS order is authoritative; tetra is 40/45
    for i, s in enumerate(FISH_SPECS):
        s["fish_idx"] = BASE_FISH_IDX + i
        s["gyo"] = BASE_GYO_TYPE + 1 + i
    total_fish_num = BASE_FISH_IDX + len(FISH_SPECS)

    for s in FISH_SPECS:
        if len(s["name"]) > 16:
            die(f"name too long (>16): {s['name']!r}")

    def missing_from(t, key=lambda s: f"aGYO_TYPE_{s['enum']}"):
        return [s for s in FISH_SPECS if key(s) not in t]

    # --- 1. enum ------------------------------------------------------------
    new_specs = missing_from(text)
    if new_specs:
        add = "".join(f"    aGYO_TYPE_{s['enum']},\n" for s in new_specs)
        text = text.replace("\n    aGYO_TYPE_MODDED_NUM", f"\n{add}\n    aGYO_TYPE_MODDED_NUM", 1)
        write(gyoei_h, text)

    # --- 2. gyoei_type ------------------------------------------------------
    p = SRC / "actor" / "ac_gyoei_type.c_inc"
    t = read(p)
    todo = missing_from(t)
    if todo:
        add = "".join(f"    {{ aGYO_SIZE_{s['size']}, {s['search']}, {s['bite']} }}, // aGYO_TYPE_{s['enum']} (modded)\n"
                      for s in todo)
        t = t.replace("};\n// clang-format on", add + "};\n// clang-format on", 1)
        write(p, t)

    # --- 3. display list ----------------------------------------------------
    p = SRC / "actor" / "ac_gyoei_model.c_inc"
    t = read(p)
    todo = missing_from(t)
    if todo:
        anchor = re.search(r"  &aGYO_tetra_dl[^\n]*NEON_TETRA[^\n]*\n", t)
        if not anchor:
            die("tetra displayList anchor missing")
        line = anchor.group(0)
        fixed = line.rstrip("\n")
        if not fixed.rstrip().endswith(","):
            fixed = re.sub(r"(\&aGYO_tetra_dl)", r"\1,", fixed, count=1)
        add = "".join(f"  &{model_dl(s['model'])}, /* aGYO_TYPE_{s['enum']} (modded) */\n" for s in todo)
        t = t.replace(line, fixed + "\n" + add, 1)
        write(p, t)

    # --- 4. uki item mapping --------------------------------------------------
    p = SRC / "actor" / "ac_uki_move.c_inc"
    t = read(p)
    todo = missing_from(t)
    if todo:
        add = "".join(f"        (mActor_name_t)(ITM_FISH_START + {s['fish_idx']}), /* aGYO_TYPE_{s['enum']} (modded) */\n"
                      for s in todo)
        t = insert_after(t, "        ITM_FISH40, /* aGYO_TYPE_NEON_TETRA (modded) */\n", add, p)
        write(p, t)

    # --- 5. release animation -------------------------------------------------
    p = SRC / "actor" / "ac_gyo_release.c"
    t = read(p)
    todo = missing_from(t)
    if todo:
        add = "".join(f"        {s['anime']}, /* aGYO_TYPE_{s['enum']} (modded) */\n" for s in todo)
        t = insert_after(t, "        1, /* aGYO_TYPE_NEON_TETRA (modded) */\n", add, p)
        write(p, t)

    # --- 6. FISH_NUM -----------------------------------------------------------
    p = INC / "m_name_table.h"
    t = read(p)
    if not re.search(rf"#define FISH_NUM {total_fish_num}\b", t):
        t = re.sub(r"#define FISH_NUM \d+[^\n]*",
                   f"#define FISH_NUM {total_fish_num} /* 40 vanilla + modded fish (see fish/ADDING_FISH.md) */",
                   t, count=1)
        write(p, t)

    # --- 7. price ---------------------------------------------------------------
    p = SRC / "data" / "item" / "fish_price.c"
    t = read(p)
    todo = [s for s in FISH_SPECS if f"/* {s['name']} (modded)" not in t]
    if todo:
        add = "".join(f"    {s['price']}, /* {s['name']} (modded): sells for {s['price'] // 4:,} Bells */\n"
                      for s in todo)
        t = t.replace("    -1,\n", add + "    -1,\n", 1)
        write(p, t)

    # --- 8. item name -------------------------------------------------------------
    p = SRC / "data" / "item" / "item_name.c"
    t = read(p)
    todo = [s for s in FISH_SPECS if f"/* {s['name']} */" not in t]
    if todo:
        lines = []
        for s in todo:
            padded = s["name"].ljust(16)
            chars = ", ".join(f"'{c}'" for c in padded)
            lines.append(f"    {chars}, /* {s['name']} */\n")
        t = insert_after(t, "/* neon tetra */\n", "".join(lines), p)
        write(p, t)

    # --- 9. article ------------------------------------------------------------------
    p = SRC / "game" / "m_item_name.c"
    t = read(p)
    todo = [s for s in FISH_SPECS if f"/* {s['name']} (modded) */" not in t]
    if todo:
        add = "".join(f"    mIN_ARTICLE_{s['article']}, /* {s['name']} (modded) */\n" for s in todo)
        t = insert_after(t, "    mIN_ARTICLE_A, /* neon tetra (modded) */\n", add, p)
        write(p, t)

    # --- 10. icon palettes (regenerated wholesale) -------------------------------------
    sub_p = SRC / "game" / "m_submenu_ovl.c"
    sub = read(sub_p)
    tbl = re.search(r"static mSM_inventory_icon_info_c fish_tex_table\[\] = \{(.*?)\n    \};", sub, re.S)
    if not tbl:
        die("fish_tex_table not found")
    rows = re.findall(r"\{ (\w+), (\w+) \}", tbl.group(1))
    if len(rows) < VANILLA_FISH:
        die("fish_tex_table too short")

    def load_base_pal(idx):
        pal_name = rows[idx][0]
        inc = REPO / "build" / "GAFE01_00" / "include" / "assets" / f"{pal_name}.inc"
        if not inc.exists():
            die(f"base palette not found: {inc}")
        return [int(v) for v in re.findall(r"\d+", inc.read_text())], rows[idx][1]

    def shift_pal(vals, deg, sat, val):
        out = []
        for i, v in enumerate(vals):
            keep = (i % 16) in (0, 1)  # transparent + background disc per 16-entry half
            if keep or not (v & 0x8000):
                out.append(v)
                continue
            r, g, b = (v >> 10) & 31, (v >> 5) & 31, v & 31
            h, s2, v2 = colorsys.rgb_to_hsv(r / 31, g / 31, b / 31)
            h = (h + deg / 360.0) % 1.0
            r2, g2, b2 = colorsys.hsv_to_rgb(h, min(1.0, s2 * sat), min(1.0, v2 * val))
            out.append(0x8000 | (round(r2 * 31) << 10) | (round(g2 * 31) << 5) | round(b2 * 31))
        return out

    pal_lines = ["/* Generated by fish/add_fish.py - do not hand-edit.",
                 " * Icon palettes for modded fish: vanilla fish icon textures recolored.",
                 " * Entries 0/16 (transparent) and 1/17 (background disc) are preserved. */",
                 ""]
    tex_of = {}
    for s in FISH_SPECS:
        base_idx, deg, sat, val = s["icon"]
        vals, tex = load_base_pal(base_idx)
        tex_of[s["enum"]] = tex
        shifted = shift_pal(vals, deg, sat, val)
        sym = f"inv_mwin_mf_{s['enum'].lower()}_pal"
        s["pal_sym"] = sym
        pal_lines.append(f"u16 {sym}[] = {{")
        for i in range(0, len(shifted), 8):
            pal_lines.append("    " + ", ".join(f"0x{v:04X}" for v in shifted[i:i + 8]) + ",")
        pal_lines.append("};")
        pal_lines.append("")
    write(SRC / "data" / "model" / "inv_mwin_modfish_pal.c_inc", "\n".join(pal_lines))

    # externs + table entries in m_submenu_ovl.c (only for fish not yet there)
    added_ext = []
    added_rows = []
    for s in FISH_SPECS:
        if s["pal_sym"] not in sub:
            added_ext.append(f"extern u16 {s['pal_sym']}[]; /* {s['name']} (modded) */\n")
            added_rows.append(f"        {{ {s['pal_sym']}, {tex_of[s['enum']]} }}, /* {s['name']} (modded) */\n")
    if added_ext:
        sub = insert_after(sub, "extern u16 inv_mwin_41tetra_pal[]; /* neon tetra (modded) */\n",
                           "".join(added_ext), sub_p)
        sub = insert_after(sub, "        { inv_mwin_41tetra_pal, inv_mwin_41tetra_tex }, /* neon tetra (modded) */\n",
                           "".join(added_rows), sub_p)
        write(sub_p, sub)

    # --- 11. spawn tables ------------------------------------------------------------------
    p = SRC / "actor" / "ac_set_ovl_gyoei.c"
    t = read(p)
    if missing_from(t, key=lambda s: f"FISH_SPAWN({s['enum']},"):

        def month_tables(letter):
            m = re.search(rf"static aSOG_term_list_c\* {letter}_month\[lbRTC_MONTHS_MAX\]\[aSOG_TERM_NUM\] = \{{(.*?)\}};",
                          t, re.S)
            return re.findall(r"\{\s*(\w+)\s*,\s*(\w+)\s*\}", m.group(1))

        def term_list(name):
            m = re.search(rf"static aSOG_term_list_c {name}\[aSOG_TIME_NUM\] = \{{(.*?)\}};", t, re.S)
            return re.findall(r"\{\s*\d+\s*,\s*(\w+)\s*\}", m.group(1))

        tables = {"r": month_tables("r"), "s": month_tables("s"), "p": month_tables("p")}
        area_letter = {"RIVER": "r", "POOL": "r", "WATERFALL": "r", "RIVER_MOUTH": "r",
                       "SEA": "s", "OFFING": "s", "POND": "p"}

        for s in FISH_SPECS:
            if f"FISH_SPAWN({s['enum']}," in t:
                continue
            letter = area_letter[s["area"]]
            targets = set()
            for month in s["months"]:
                for list_name in tables[letter][month - 1]:
                    if list_name == "NULL":
                        print(f"  warning: {s['enum']}: no {letter} table for month {month} half - skipped")
                        continue
                    slots = term_list(list_name)
                    for slot in s["slots"]:
                        targets.add(slots[slot])
            line = f"  FISH_SPAWN({s['enum']}, {s['area']}, {s['weight']}), /* modded */\n"
            for arr in sorted(targets):
                block = re.search(rf"(static aSOG_term_info_c {arr}\[\d*\] = \{{.*?)(\}};)", t, re.S)
                if not block:
                    die(f"spawn array {arr} not found")
                if f"FISH_SPAWN({s['enum']}," in block.group(1):
                    continue
                t = t[:block.end(1)] + line + t[block.end(1):]

        # fix up array sizes and term-list counts
        counts = {}
        for m in re.finditer(r"static aSOG_term_info_c (\w+)\[\d*\] = \{(.*?)\};", t, re.S):
            counts[m.group(1)] = len(re.findall(r"FISH_SPAWN\(", m.group(2)))
        t = re.sub(r"static aSOG_term_info_c (\w+)\[\d*\]",
                   lambda m: f"static aSOG_term_info_c {m.group(1)}[{counts[m.group(1)]}]", t)
        t = re.sub(r"\{ (\d+), (\w+) \}",
                   lambda m: f"{{ {counts[m.group(2)]}, {m.group(2)} }}" if m.group(2) in counts else m.group(0), t)
        write(p, t)

    # --- 12. encyclopedia page-2 slots (regenerated) -----------------------------------------
    p = SRC / "game" / "m_inventory_ovl.c"
    t = read(p)
    all_mod = ["NEON_TETRA"] + [s["enum"] for s in FISH_SPECS]
    if len(all_mod) > 40:
        die("more than 40 modded fish: add a third encyclopedia page (mIV_FISH_PAGE_NUM)")
    entries = [f"aGYO_TYPE_{e}" for e in all_mod] + ["E"] * (40 - len(all_mod))
    body = ""
    for i in range(0, 40, 4):
        body += "    " + ", ".join(entries[i:i + 4]) + ",\n"
    t = re.sub(r"(static u8 mIV_fish_collect_list2\[mIV_COLLECT_NUM\] = \{\n).*?(\};)",
               lambda m: m.group(1) + body + m.group(2), t, flags=re.S)
    write(p, t)

    # --- 13. gen_fish_table display names ------------------------------------------------------
    p = REPO / "fish" / "gen_fish_table.py"
    t = read(p)
    add = "".join(f'    "{s["enum"]}": "{s["display"]}",\n' for s in FISH_SPECS if f'"{s["enum"]}"' not in t)
    if add:
        t = insert_after(t, '    "NEON_TETRA": "Neon tetra",\n', add, p)
        write(p, t)

    print(f"\ndone: FISH_NUM = {total_fish_num}")
    print("next: python fish/gen_fish_table.py --write && python fish/make_iso.py")


if __name__ == "__main__":
    main()
