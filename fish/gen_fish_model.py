#!/usr/bin/env python3
"""gen_fish_model.py — Generate a complete AC GameCube fish model as a C file.

Produces src/data/model/act_f<NN>_<name>.c containing:
  * a 16-color RGB5A3 palette (index 0 = transparent)
  * a 32x32 CI4 texture, painted procedurally from the spec and swizzled
    into the GameCube's native 8x8 pixel blocks
  * three Vtx frames (tail bent up / neutral / bent down) of a low-poly,
    double-sided, side-profile fish mesh whose UVs match the painted texture
  * three display lists (aT/bT/cT) in the exact style of the vanilla
    act_f##_* fish models (same combiner / render mode / TLUT commands)

The mesh + texture come from the same parametric outline, so the silhouette
always matches. Add a new entry to SPECS and run:

    python fish/gen_fish_model.py tetra
    python fish/gen_fish_model.py --list

The script prints the aGYO_DL_c registration snippet to paste into
src/actor/ac_gyoei_model.c_inc.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "src" / "data" / "model"

TEX_W = TEX_H = 32


def rgb(r5, g5, b5):
    """Opaque RGB555 palette entry (0-31 channels)."""
    return 0x8000 | (r5 << 10) | (g5 << 5) | b5


# ---------------------------------------------------------------------------
# Fish specs. All colors are (r,g,b) in 0-31. Roles paint the texture:
#   back    - upper body        belly - lower body      stripe - lateral line
#   rear    - rear-lower body + tail   outline - silhouette edge
#   eye     - eye dot           fin   - tail fin shading
# Geometry: length/height in model units (~560 = killifish-sized when the
# engine draws at its standard fish scales).
# ---------------------------------------------------------------------------
SPECS = {
    "tetra": {
        "num": 41,
        "display_name": "neon tetra",
        "length": 455,
        "height": 175,
        "tail_x": 0.48,      # fraction of half-length where the tail fin starts
        "belly_scale": 0.78,
        "blunt_head": True,
        "red_tail": True,
        "colors": {
            "outline": rgb(6, 8, 12),
            "back": rgb(6, 12, 9),
            "belly": rgb(26, 29, 28),
            "stripe": rgb(6, 24, 30),
            "stripe2": rgb(18, 30, 30),
            "rear": rgb(25, 4, 3),
            "rear2": rgb(30, 9, 4),
            "eye": rgb(2, 2, 2),
            "eye_white": rgb(30, 30, 27),
            "fin": rgb(24, 24, 24),
            "fin2": rgb(20, 24, 26),
        },
    },
    "pike": {
        "num": 42,
        "display_name": "pike",
        "length": 690,
        "height": 205,
        "tail_x": 0.60,
        "belly_scale": 0.78,
        "pike_spots": True,
        "brown_tail": True,
        "colors": {
            "outline": rgb(5, 6, 4),
            "back": rgb(8, 12, 5),
            "belly": rgb(26, 27, 19),
            "stripe": rgb(13, 15, 8),
            "stripe2": rgb(18, 19, 11),
            "rear": rgb(19, 12, 4),
            "rear2": rgb(25, 20, 10),
            "eye": rgb(2, 2, 1),
            "eye_white": rgb(28, 27, 21),
            "fin": rgb(13, 8, 3),
        },
    },
}


# ---------------------------------------------------------------------------
# Texture painting + swizzling
# ---------------------------------------------------------------------------

def outline_test(fx, fy, spec):
    """Return region id for a point in fish space. fx in [-1,1] nose->tail,
    fy in [-1,1] bottom->top. Region: '' outside, 'body', 'tail'."""
    tail_x = spec["tail_x"]
    if fx < tail_x:
        # body: tapered ellipse. Tiny ornamental fish can ask for a blunter,
        # toy-like head to match the vanilla gupi/kingyo icon language.
        t = (fx + 1.0) / (tail_x + 1.0)          # 0 at nose, 1 at peduncle
        head_floor = 0.24 if spec.get("blunt_head") else 0.08
        body_pow = 0.55 if spec.get("blunt_head") else 0.8
        half = math.sin(min(t * 1.18, 1.0) * math.pi * 0.5) ** body_pow
        half = max(half, head_floor)
        peduncle = 0.42 + 0.58 * (1.0 - max(0.0, (t - 0.70) / 0.30))
        half *= min(1.0, peduncle)
        if fy < 0:
            half *= spec.get("belly_scale", 1.0)
        return "body" if abs(fy) <= half else ""
    else:
        # tail fin: widening triangle from the peduncle
        t = (fx - tail_x) / (1.0 - tail_x)       # 0 at peduncle, 1 at tip
        half = 0.24 + 0.55 * t
        return "tail" if abs(fy) <= half else ""


def paint_texture(spec):
    """Return (pixels[32*32] of palette indices, palette list)."""
    c = spec["colors"]
    palette = [0x0000, c["outline"], c["back"], c["belly"], c["stripe"],
               c["stripe2"], c["rear"], c["rear2"], c["eye"], c["fin"],
               c["eye_white"], c.get("fin2", c["fin"]), 0, 0, 0, 0]
    OUTLINE, BACK, BELLY, STRIPE, STRIPE2, REAR, REAR2, EYE, FIN, EYE_WHITE, FIN2 = range(1, 12)

    px = [0] * (TEX_W * TEX_H)

    def region(x, y):
        fx = (x + 0.5) / TEX_W * 2.0 - 1.0
        fy = 1.0 - (y + 0.5) / TEX_H * 2.0
        return outline_test(fx, fy, spec), fx, fy

    for y in range(TEX_H):
        for x in range(TEX_W):
            reg, fx, fy = region(x, y)
            if not reg:
                continue
            if reg == "tail":
                t = (fx - spec["tail_x"]) / (1.0 - spec["tail_x"])
                if spec.get("red_tail"):
                    col = REAR2 if int(x + y) % 3 == 0 else REAR
                elif spec.get("brown_tail"):
                    col = REAR2 if fy > -0.10 else REAR
                    if t > 0.28 and int(x + y) % 3 == 0:
                        col = FIN
                else:
                    col = FIN if (int(x + y) % 3 == 0 and t > 0.25) else (STRIPE2 if fy > -0.15 else FIN)
            else:
                if spec.get("pike_spots"):
                    if fy > 0.32:
                        col = BACK
                    elif fy > -0.14:
                        col = STRIPE if fx < 0.10 else STRIPE2
                    else:
                        col = BELLY
                    body_t = (fx + 1.0) / (spec["tail_x"] + 1.0)
                    if 0.12 < body_t < 0.90 and -0.42 < fy < 0.34 and ((x * 3 + y * 5) % 11 in (0, 1)):
                        col = EYE_WHITE if fy < 0.18 else STRIPE2
                else:
                    band_top = 0.30 - 0.06 * math.sin((fx + 0.2) * math.pi)
                    band_bottom = 0.00 + 0.05 * math.sin((fx + 0.8) * math.pi * 0.7)
                    if band_bottom <= fy <= band_top and not (fx > 0.04 and fy < 0.10):
                        col = STRIPE if fx < 0.20 else STRIPE2   # broken chunky side highlight
                    elif fy > 0:
                        col = BACK
                    else:
                        # neon tetra: red lower rear and tail base from the approved icon.
                        col = REAR if (0.22 < fx < spec["tail_x"] and -0.55 < fy < -0.10) else BELLY
            px[y * TEX_W + x] = col

    # outline pass: any painted pixel adjacent to background becomes outline
    out = px[:]
    for y in range(TEX_H):
        for x in range(TEX_W):
            if px[y * TEX_W + x] == 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < TEX_W and 0 <= ny < TEX_H) or px[ny * TEX_W + nx] == 0:
                    out[y * TEX_W + x] = OUTLINE
                    break
    px = out

    # eye near the nose, on the stripe line
    eye_white = {
        (5, 14), (6, 14),
        (5, 15), (6, 15),
    }
    eye_pupil = {(6, 15)}
    for xx, yy in eye_white:
        if px[yy * TEX_W + xx] != 0:
            px[yy * TEX_W + xx] = EYE_WHITE
    for xx, yy in eye_pupil:
        if px[yy * TEX_W + xx] != 0:
            px[yy * TEX_W + xx] = EYE

    # Small approved-style fins: blue-gray above, light gray below.
    top_fins = {
        (18, 11), (19, 11), (20, 11),
        (18, 12), (19, 12),
    }
    bottom_fins = {
        (20, 20), (21, 20), (22, 20),
        (21, 21), (22, 21),
    }
    for xx, yy in top_fins:
        if px[yy * TEX_W + xx] != 0:
            px[yy * TEX_W + xx] = FIN2
    for xx, yy in bottom_fins:
        if px[yy * TEX_W + xx] != 0:
            px[yy * TEX_W + xx] = FIN

    return px, palette


def swizzle_ci4(px):
    """Linear palette indices -> GC CI4 bytes (8x8 pixel blocks, 2 px/byte)."""
    data = bytearray()
    for by in range(TEX_H // 8):
        for bx in range(TEX_W // 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    p0 = px[(by * 8 + y) * TEX_W + bx * 8 + x]
                    p1 = px[(by * 8 + y) * TEX_W + bx * 8 + x + 1]
                    data.append((p0 << 4) | p1)
    return bytes(data)


# ---------------------------------------------------------------------------
# Mesh
# ---------------------------------------------------------------------------

def build_mesh(spec):
    """Return (verts [(x,y)], tris [(a,b,c)], tail_flags [bool per vert]).
    Fish faces +X (nose at -x, tail at +x), in the XY plane."""
    L2 = spec["length"] / 2.0
    H2 = spec["height"] / 2.0
    tx = spec["tail_x"] * L2                      # peduncle x
    belly_scale = spec.get("belly_scale", 1.0)
    if spec.get("blunt_head"):
        verts = [
            (-L2, H2 * 0.20),                      # 0 blunt snout top
            (-L2 * 0.62, H2 * 0.88),               # 1 top front
            (L2 * 0.08, H2 * 0.78),                # 2 top rear
            (tx, H2 * 0.28),                       # 3 peduncle top
            (L2, H2 * 0.58),                       # 4 tail tip top
            (L2, -H2 * 0.54),                      # 5 tail tip bottom
            (tx, -H2 * 0.24 * belly_scale),        # 6 peduncle bottom
            (L2 * 0.06, -H2 * 0.74 * belly_scale), # 7 bottom rear
            (-L2 * 0.56, -H2 * 0.86 * belly_scale),# 8 bottom front
            (-L2, -H2 * 0.20),                     # 9 blunt snout bottom
        ]
        tris = [
            (0, 1, 9), (1, 8, 9), (1, 2, 8), (2, 7, 8), (2, 3, 7), (3, 6, 7),
            (3, 4, 5), (3, 5, 6),
        ]
        tris += [(a, c, b) for (a, b, c) in tris]
        tail = [False, False, False, True, True, True, True, False, False, False]
        return verts, tris, tail

    verts = [
        (-L2, 0),                                 # 0 nose
        (-L2 * 0.42, H2 * 0.9),                   # 1 top front
        (L2 * 0.28, H2 * 0.7),                    # 2 top rear
        (tx, H2 * 0.30),                          # 3 peduncle top
        (L2, H2 * 0.95),                          # 4 tail tip top
        (L2, -H2 * 0.95),                         # 5 tail tip bottom
        (tx, -H2 * 0.30 * belly_scale),           # 6 peduncle bottom
        (L2 * 0.28, -H2 * 0.7 * belly_scale),     # 7 bottom rear
        (-L2 * 0.42, -H2 * 0.9 * belly_scale),    # 8 bottom front
    ]
    tris = [
        (0, 1, 8), (1, 2, 8), (2, 7, 8), (2, 3, 7), (3, 6, 7),
        (3, 4, 5), (3, 5, 6),
    ]
    # double-sided: same triangles, reversed winding
    tris += [(a, c, b) for (a, b, c) in tris]
    tail = [False, False, False, True, True, True, True, False, False]
    return verts, tris, tail


def make_frame(verts, tail, spec, bend):
    """Return list of Vtx tuples for one animation frame."""
    L2 = spec["length"] / 2.0
    tx = spec["tail_x"] * L2
    out = []
    for (x, y), is_tail in zip(verts, tail):
        z = 0.0
        if is_tail and bend != 0:
            z = bend * 40.0 * (x - tx) / (L2 - tx)
        # UVs: map (x,y) onto the 32x32 texture (tc = texel * 32)
        s = int(round((x / L2 * 0.5 + 0.5) * (TEX_W - 0.01) * 32))
        t = int(round((0.5 - y / spec["height"]) * (TEX_H - 0.01) * 32))
        out.append((int(round(x)), int(round(y)), int(round(z)), 1, s, t, 255, 255, 255, 255))
    return out


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------

def emit_tris(tris):
    """Pack triangles into gsSPNTrianglesInit_5b/gsSPNTriangles_5b lines."""
    total = len(tris)
    flat = [i for t in tris for i in t]
    lines = []
    head = flat[:9] + [0] * (9 - len(flat[:9]))
    lines.append(f"    gsSPNTrianglesInit_5b({total}, "
                 + ", ".join(str(v) for v in head) + "),")
    rest = flat[9:]
    while rest:
        chunk = rest[:12]
        rest = rest[12:]
        chunk += [0] * (12 - len(chunk))
        lines.append("    gsSPNTriangles_5b(" + ", ".join(str(v) for v in chunk) + "),")
    return lines


def emit_model(name, spec):
    px, palette = paint_texture(spec)
    tex = swizzle_ci4(px)
    verts, tris, tail = build_mesh(spec)
    num = spec["num"]
    base = f"act_f{num}_{name}"

    frames = {"a": make_frame(verts, tail, spec, +1.0),
              "b": make_frame(verts, tail, spec, 0.0),
              "c": make_frame(verts, tail, spec, -1.0)}

    o = []
    o.append("/* Generated by fish/gen_fish_model.py - do not hand-edit.")
    o.append(f" * Fish model: {spec['display_name']} (fish #{num}, modded)")
    o.append(f" * Regenerate: python fish/gen_fish_model.py {name} */")
    o.append('#include "libforest/gbi_extensions.h"')
    o.append('#include "PR/gbi.h"')
    o.append("")
    o.append(f"static u16 {base}_pal[16] ATTRIBUTE_ALIGN(32) = {{")
    o.append("    " + ", ".join(f"0x{v:04X}" for v in palette) + ",")
    o.append("};")
    o.append("")
    o.append(f"static u8 {base}_tex[{len(tex)}] ATTRIBUTE_ALIGN(32) = {{")
    for i in range(0, len(tex), 16):
        o.append("    " + ", ".join(f"0x{b:02X}" for b in tex[i:i + 16]) + ",")
    o.append("};")

    tri_lines = emit_tris(tris)
    for f in ("a", "b", "c"):
        o.append("")
        o.append(f"static Vtx {base}_{f}_v[{len(verts)}] = {{")
        for v in frames[f]:
            o.append("    { " + ", ".join(str(x) for x in v) + " },")
        o.append("};")
        o.append("")
        o.append(f"Gfx {base}_{f}T_model[] = {{")
        o.append("    gsSPTexture(0, 0, 0, G_TX_RENDERTILE, G_ON),")
        o.append("    gsDPSetRenderMode(G_RM_FOG_SHADE_A, G_RM_AA_ZB_TEX_EDGE2),")
        o.append("    gsDPSetCombineLERP(TEXEL0, 0, SHADE, 0, 0, 0, 0, TEXEL0, PRIMITIVE, 0, COMBINED, 0, 0, 0, 0, COMBINED),")
        o.append(f"    gsDPLoadTLUT_Dolphin(15, 16, 1, {base}_pal),")
        o.append(f"    gsDPSetTextureImage_Dolphin(G_IM_FMT_CI, G_IM_SIZ_4b, {TEX_W}, {TEX_H}, {base}_tex),")
        o.append("    gsDPSetTile_Dolphin(G_DOLPHIN_TLUT_DEFAULT_MODE, 0, 15, GX_CLAMP, GX_CLAMP, 0, 0),")
        o.append("    gsDPSetPrimColor(0, 128, 255, 255, 255, 255),")
        o.append("    gsSPLoadGeometryMode(G_ZBUFFER | G_SHADE | G_CULL_BACK | G_FOG | G_SHADING_SMOOTH),")
        o.append(f"    gsSPVertex({base}_{f}_v, {len(verts)}, 0),")
        o.extend(tri_lines)
        o.append("    gsSPEndDisplayList(),")
        o.append("};")

    out_path = OUT_DIR / f"{base}.c"
    out_path.write_text("\n".join(o) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    print("\nRegister in src/actor/ac_gyoei_model.c_inc:")
    print(f"  extern Gfx {base}_aT_model[];  /* + bT/cT */")
    print(f"  static aGYO_DL_c aGYO_{name}_dl = {{ {base}_aT_model, {base}_bT_model, {base}_cT_model }};")
    print(f"  -> set the fish's aGYO_displayList entry to &aGYO_{name}_dl")
    print(f"\nInclude the model in the build: add to src/f_furniture.c:")
    print(f'  #include "../src/data/model/{base}.c"')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", nargs="?", help="spec name (see SPECS)")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or not args.name:
        print("available specs:", ", ".join(SPECS))
        return 0 if args.list else 1
    if args.name not in SPECS:
        sys.exit(f"unknown spec '{args.name}' (have: {', '.join(SPECS)})")
    emit_model(args.name, SPECS[args.name])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
