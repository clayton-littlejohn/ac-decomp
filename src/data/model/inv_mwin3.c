#include "libforest/gbi_extensions.h"
#include "PR/gbi.h"
#include "evw_anime.h"
#include "c_keyframe.h"
#include "ac_npc.h"
#include "ef_effect_control.h"

u16 inv_mwin_08oonamazu_pal[] ATTRIBUTE_ALIGN(32) = {
#include "assets/inv_mwin_08oonamazu_pal.inc"
};

u16 inv_mwin_01funa_pal[] = {
#include "assets/inv_mwin_01funa_pal.inc"
};

u16 inv_mwin_02masu_pal[] = {
#include "assets/inv_mwin_02masu_pal.inc"
};

u16 inv_mwin_03koi_pal[] = {
#include "assets/inv_mwin_03koi_pal.inc"
};

u16 inv_mwin_04nishiki_pal[] = {
#include "assets/inv_mwin_04nishiki_pal.inc"
};

u16 inv_mwin_05nigoi_pal[] = {
#include "assets/inv_mwin_05nigoi_pal.inc"
};

u16 inv_mwin_06ugui_pal[] = {
#include "assets/inv_mwin_06ugui_pal.inc"
};

u16 inv_mwin_07namazu_pal[] = {
#include "assets/inv_mwin_07namazu_pal.inc"
};

u16 inv_mwin_09oikawa_pal[] = {
#include "assets/inv_mwin_09oikawa_pal.inc"
};

u16 inv_mwin_10tanago_pal[] = {
#include "assets/inv_mwin_10tanago_pal.inc"
};

u16 inv_mwin_11dojyou_pal[] = {
#include "assets/inv_mwin_11dojyou_pal.inc"
};

u16 inv_mwin_12gill_pal[] = {
#include "assets/inv_mwin_12gill_pal.inc"
};

u16 inv_mwin_13bass_pal[] = {
#include "assets/inv_mwin_13bass_pal.inc"
};

u16 inv_mwin_14bassm_pal[] = {
#include "assets/inv_mwin_14bassm_pal.inc"
};

u16 inv_mwin_15bassl_pal[] = {
#include "assets/inv_mwin_15bassl_pal.inc"
};

u16 inv_mwin_16raigyo_pal[] = {
#include "assets/inv_mwin_16raigyo_pal.inc"
};

u16 inv_mwin_17unagi_pal[] = {
#include "assets/inv_mwin_17unagi_pal.inc"
};

u16 inv_mwin_18donko_pal[] = {
#include "assets/inv_mwin_18donko_pal.inc"
};

u16 inv_mwin_19wakasagi_pal[] = {
#include "assets/inv_mwin_19wakasagi_pal.inc"
};

u16 inv_mwin_20ayu_pal[] = {
#include "assets/inv_mwin_20ayu_pal.inc"
};

u16 inv_mwin_21yamame_pal[] = {
#include "assets/inv_mwin_21yamame_pal.inc"
};

u16 inv_mwin_22niji_pal[] = {
#include "assets/inv_mwin_22niji_pal.inc"
};

u16 inv_mwin_23iwana_pal[] = {
#include "assets/inv_mwin_23iwana_pal.inc"
};

u16 inv_mwin_24itou_pal[] = {
#include "assets/inv_mwin_24itou_pal.inc"
};

u16 inv_mwin_25sake_pal[] = {
#include "assets/inv_mwin_25sake_pal.inc"
};

u16 inv_mwin_26kingyo_pal[] = {
#include "assets/inv_mwin_26kingyo_pal.inc"
};

u16 inv_mwin_27demekin_pal[] = {
#include "assets/inv_mwin_27demekin_pal.inc"
};

u16 inv_mwin_28gupi_pal[] = {
#include "assets/inv_mwin_28gupi_pal.inc"
};

/* neon tetra (modded): custom icon texture with a muted teal/cyan palette.
 * Entries 1 and 17 are the icon's background disc and MUST stay identical to
 * the vanilla fish icons (dark blue) so the item background matches. */
u16 inv_mwin_41tetra_pal[] = {
    0x0000, 0xB19F, 0x8D49, 0xC0A4, 0xEBBC, 0xE483, 0xF924, 0xE318,
    0x8842, 0xD31A, 0xA12B, 0x9989, 0xA1ED, 0xC2F6, 0x9B1E, 0xCBDE,
    0x0000, 0xA66D, 0x8D49, 0xC0A4, 0xEBBC, 0xE483, 0xF924, 0xE318,
    0x8842, 0xD31A, 0xA12B, 0x9989, 0xA1ED, 0xC2F6, 0x9B1E, 0xCBDE,
};

/* Custom 32x32 CI4 icon texture for neon tetra.
 * Uses the same swizzled 8x8-block layout as the vanilla inventory icons. */
u8 inv_mwin_41tetra_tex[512] = {
#include "../src/data/model/inv_mwin_41tetra_tex.c_inc"
};

/* Pike (modded): approved custom icon based on the vanilla raigyo structure. */
u16 inv_mwin_42pike_pal[] = {
    0x0000, 0xB19F, 0x94C4, 0xA125, 0xA986, 0xB9E8, 0xCA6C, 0xDAD0,
    0xEF54, 0xC165, 0xA8E3, 0x8C62, 0xEF75, 0xB1C8, 0xD629, 0xE6EF,
    0x0000, 0xA66D, 0x94C4, 0xA125, 0xA986, 0xB9E8, 0xCA6C, 0xDAD0,
    0xEF54, 0xC165, 0xA8E3, 0x8C62, 0xEF75, 0xB1C8, 0xD629, 0xE6EF,
};

u8 inv_mwin_42pike_tex[512] = {
#include "../src/data/model/inv_mwin_42pike_tex.c_inc"
};

/* Yellow perch (modded): approved custom icon based on the vanilla ugui structure. */
u16 inv_mwin_43perch_pal[] = {
    0x0000, 0xB19F, 0x9CA3, 0xA504, 0xB565, 0xC9C7, 0xDA49, 0xEACB,
    0xF750, 0xCD25, 0xB0E4, 0x8C62, 0xF774, 0xB124, 0xA0C4, 0xD9C7,
    0x0000, 0xA66D, 0x9CA3, 0xA504, 0xB565, 0xC9C7, 0xDA49, 0xEACB,
    0xF750, 0xCD25, 0xB0E4, 0x8C62, 0xF774, 0xB124, 0xA0C4, 0xD9C7,
};

u8 inv_mwin_43perch_tex[512] = {
#include "../src/data/model/inv_mwin_43perch_tex.c_inc"
};

/* Sturgeon (modded): approved custom icon based on the vanilla itou structure. */
u16 inv_mwin_44sturgeon_pal[] = {
    0x0000, 0xB19F, 0x9483, 0xA4C4, 0xB126, 0xBD89, 0xCA0D, 0xDAB3,
    0xE716, 0xB526, 0xA0C5, 0x8C42, 0xEF58, 0xB98A, 0xA905, 0xCA0C,
    0x0000, 0xA66D, 0x9483, 0xA4C4, 0xB126, 0xBD89, 0xCA0D, 0xDAB3,
    0xE716, 0xB526, 0xA0C5, 0x8C42, 0xEF58, 0xB98A, 0xA905, 0xCA0C,
};

u8 inv_mwin_44sturgeon_tex[512] = {
#include "../src/data/model/inv_mwin_44sturgeon_tex.c_inc"
};

/* Golden trout (modded): approved custom icon based on the vanilla niji structure. */
u16 inv_mwin_45golden_trout_pal[] = {
    0x0000, 0xB19F, 0x8C62, 0xA0E4, 0xB145, 0xB965, 0xD249, 0xF3B4,
    0xEACD, 0xD1E8, 0xA8C4, 0xC105, 0xB98A, 0xF39A, 0x8441, 0x8D5F,
    0x0000, 0xA66D, 0x8C62, 0xA0E4, 0xB145, 0xB965, 0xD249, 0xF3B4,
    0xEACD, 0xD1E8, 0xA8C4, 0xC105, 0xB98A, 0xF39A, 0x8441, 0x8D5F,
};

u8 inv_mwin_45golden_trout_tex[512] = {
#include "../src/data/model/inv_mwin_45golden_trout_tex.c_inc"
};

/* Tilapia (modded): approved custom icon based on the vanilla tai structure. */
u16 inv_mwin_46tilapia_pal[] = {
    0x0000, 0xB19F, 0x9484, 0xA4E7, 0xB169, 0xBDED, 0xCE71, 0xDEF5,
    0xEF58, 0xB929, 0xD18A, 0xEE4F, 0x8C42, 0xF779, 0xA908, 0xC5CC,
    0x0000, 0xA66D, 0x9484, 0xA4E7, 0xB169, 0xBDED, 0xCE71, 0xDEF5,
    0xEF58, 0xB929, 0xD18A, 0xEE4F, 0x8C42, 0xF779, 0xA908, 0xC5CC,
};

u8 inv_mwin_46tilapia_tex[512] = {
#include "../src/data/model/inv_mwin_46tilapia_tex.c_inc"
};

/* modded fish icon palettes generated by fish/add_fish.py */
#include "../src/data/model/inv_mwin_modfish_pal.c_inc"

u16 inv_mwin_29angel_pal[] = {
#include "assets/inv_mwin_29angel_pal.inc"
};

u16 inv_mwin_30pirania_pal[] = {
#include "assets/inv_mwin_30pirania_pal.inc"
};

u16 inv_mwin_31aroana_pal[] = {
#include "assets/inv_mwin_31aroana_pal.inc"
};

u16 inv_mwin_32kaseki_pal[] = {
#include "assets/inv_mwin_32kaseki_pal.inc"
};

u8 inv_mwin_08oonamazu_tex[] = {
#include "assets/inv_mwin_08oonamazu_tex.inc"
};

u8 inv_mwin_01funa_tex[] = {
#include "assets/inv_mwin_01funa_tex.inc"
};

u8 inv_mwin_02masu_tex[] = {
#include "assets/inv_mwin_02masu_tex.inc"
};

u8 inv_mwin_03koi_tex[] = {
#include "assets/inv_mwin_03koi_tex.inc"
};

u8 inv_mwin_04nishiki_tex[] = {
#include "assets/inv_mwin_04nishiki_tex.inc"
};

u8 inv_mwin_05nigoi_tex[] = {
#include "assets/inv_mwin_05nigoi_tex.inc"
};

u8 inv_mwin_06ugui_tex[] = {
#include "assets/inv_mwin_06ugui_tex.inc"
};

u8 inv_mwin_07namazu_tex[] = {
#include "assets/inv_mwin_07namazu_tex.inc"
};

u8 inv_mwin_09oikawa_tex[] = {
#include "assets/inv_mwin_09oikawa_tex.inc"
};

u8 inv_mwin_10tanago_tex[] = {
#include "assets/inv_mwin_10tanago_tex.inc"
};

u8 inv_mwin_11dojyou_tex[] = {
#include "assets/inv_mwin_11dojyou_tex.inc"
};

u8 inv_mwin_12gill_tex[] = {
#include "assets/inv_mwin_12gill_tex.inc"
};

u8 inv_mwin_13bass_tex[] = {
#include "assets/inv_mwin_13bass_tex.inc"
};

u8 inv_mwin_14bassm_tex[] = {
#include "assets/inv_mwin_14bassm_tex.inc"
};

u8 inv_mwin_15bassl_tex[] = {
#include "assets/inv_mwin_15bassl_tex.inc"
};

u8 inv_mwin_16raigyo_tex[] = {
#include "assets/inv_mwin_16raigyo_tex.inc"
};

u8 inv_mwin_17unagi_tex[] = {
#include "assets/inv_mwin_17unagi_tex.inc"
};

u8 inv_mwin_18donko_tex[] = {
#include "assets/inv_mwin_18donko_tex.inc"
};

u8 inv_mwin_19wakasagi_tex[] = {
#include "assets/inv_mwin_19wakasagi_tex.inc"
};

u8 inv_mwin_20ayu_tex[] = {
#include "assets/inv_mwin_20ayu_tex.inc"
};

u8 inv_mwin_21yamame_tex[] = {
#include "assets/inv_mwin_21yamame_tex.inc"
};

u8 inv_mwin_22niji_tex[] = {
#include "assets/inv_mwin_22niji_tex.inc"
};

u8 inv_mwin_23iwana_tex[] = {
#include "assets/inv_mwin_23iwana_tex.inc"
};

u8 inv_mwin_24itou_tex[] = {
#include "assets/inv_mwin_24itou_tex.inc"
};

u8 inv_mwin_25sake_tex[] = {
#include "assets/inv_mwin_25sake_tex.inc"
};

u8 inv_mwin_26kingyo_tex[] = {
#include "assets/inv_mwin_26kingyo_tex.inc"
};

u8 inv_mwin_27demekin_tex[] = {
#include "assets/inv_mwin_27demekin_tex.inc"
};

u8 inv_mwin_28gupi_tex[] = {
#include "assets/inv_mwin_28gupi_tex.inc"
};

u8 inv_mwin_29angel_tex[] = {
#include "assets/inv_mwin_29angel_tex.inc"
};

u8 inv_mwin_30pirania_tex[] = {
#include "assets/inv_mwin_30pirania_tex.inc"
};

u8 inv_mwin_31aroana_tex[] = {
#include "assets/inv_mwin_31aroana_tex.inc"
};

u8 inv_mwin_32kaseki_tex[] = {
#include "assets/inv_mwin_32kaseki_tex.inc"
};
