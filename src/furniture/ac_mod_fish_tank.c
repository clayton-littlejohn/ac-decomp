/**
 * ac_mod_fish_tank.c - shared aquarium furniture for MODDED fish (fish idx 40+).
 *
 * Vanilla fish tanks are per-species rigged models. Modded fish instead share
 * this ONE furniture implementation: a simple vertex-colored tank drawn by a
 * custom draw_proc which also renders the fish's own act_f## swim model
 * (3-frame tail animation) gliding back and forth inside the water.
 *
 * Adding another modded fish requires NO new furniture code - just:
 *   1. append X(FTR_MOD_FISH<nn>) to the FTR1 enum (include/m_name_table.h)
 *   2. append FTR_MOD_FISH<nn> to the kind enum (include/m_ftr_def.h)
 *   3. append &iam_mod_fish00 to furniture_quality[] (profile is shared)
 * The fish species is derived from the furniture kind index at draw time.
 *
 * This file is #included by src/f_furniture.c (like all furniture TUs).
 * See fish/ADDING_FISH.md.
 */

#include "ac_furniture.h"
#include "ac_gyoei.h"
#include "m_name_table.h"
#include "m_ftr_def.h"
#include "sys_matrix.h"
#include "graph.h"
#include "m_rcp.h"

/* Fish swim models (static per-TU copy, same pattern as ac_handOverItem.c) */
#include "../src/actor/ac_gyoei_model.c_inc"

/* compile-time check: the FTR1 item enum and the furniture kind enum must
 * stay aligned for the modded fish range (see mRmTp_FtrItemNo2FtrIdx) */
typedef char aFTRMOD_kind_align_check[((0x400 + ((FTR_START(FTR_MOD_FISH00) - FTR1_START) >> 2)) == FTR_MOD_FISH00)
                                          ? 1
                                          : -1];

/* --- tank geometry (world units; one floor tile = 40) --------------------- */

/* opaque base: stand + gravel bed */
static Vtx aFTRMOD_tank_base_v[] = {
    /* stand top ring (y=4) / bottom (y=0), gray-blue */
    { -16, 4, -10, 1, 0, 0, 70, 74, 96, 255 },  { 16, 4, -10, 1, 0, 0, 70, 74, 96, 255 },
    { 16, 4, 10, 1, 0, 0, 88, 92, 114, 255 },   { -16, 4, 10, 1, 0, 0, 88, 92, 114, 255 },
    { -16, 0, -10, 1, 0, 0, 42, 44, 60, 255 },  { 16, 0, -10, 1, 0, 0, 42, 44, 60, 255 },
    { 16, 0, 10, 1, 0, 0, 52, 55, 72, 255 },    { -16, 0, 10, 1, 0, 0, 52, 55, 72, 255 },
    /* gravel bed (y=5), sandy */
    { -14, 5, -8, 1, 0, 0, 168, 148, 104, 255 }, { 14, 5, -8, 1, 0, 0, 168, 148, 104, 255 },
    { 14, 5, 8, 1, 0, 0, 196, 176, 128, 255 },   { -14, 5, 8, 1, 0, 0, 196, 176, 128, 255 },
};

static Gfx aFTRMOD_tank_base_model[] = {
    gsSPTexture(0, 0, 0, G_TX_RENDERTILE, G_OFF),
    gsDPPipeSync(),
    gsDPSetCombineLERP(0, 0, 0, SHADE, 0, 0, 0, SHADE, 0, 0, 0, SHADE, 0, 0, 0, SHADE),
    gsDPSetRenderMode(G_RM_FOG_SHADE_A, G_RM_AA_ZB_OPA_SURF2),
    gsSPLoadGeometryMode(G_ZBUFFER | G_SHADE | G_FOG | G_SHADING_SMOOTH),
    gsSPVertex(aFTRMOD_tank_base_v, 12, 0),
    /* stand top + sides (double-sided not needed: no culling set) */
    gsSPNTrianglesInit_5b(10, 0, 1, 2, 0, 2, 3, 0, 5, 1),
    gsSPNTriangles_5b(0, 4, 5, 1, 6, 2, 1, 5, 6, 2, 7, 3),
    gsSPNTriangles_5b(2, 6, 7, 3, 4, 0, 3, 7, 4, 8, 9, 10),
    gsSPNTriangles_5b(8, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    gsSPEndDisplayList(),
};

/* translucent water block above the base */
static Vtx aFTRMOD_tank_water_v[] = {
    { -15, 24, -9, 1, 0, 0, 96, 170, 235, 110 }, { 15, 24, -9, 1, 0, 0, 96, 170, 235, 110 },
    { 15, 24, 9, 1, 0, 0, 130, 200, 250, 110 },  { -15, 24, 9, 1, 0, 0, 130, 200, 250, 110 },
    { -15, 5, -9, 1, 0, 0, 70, 130, 200, 110 },  { 15, 5, -9, 1, 0, 0, 70, 130, 200, 110 },
    { 15, 5, 9, 1, 0, 0, 90, 160, 220, 110 },    { -15, 5, 9, 1, 0, 0, 90, 160, 220, 110 },
};

static Gfx aFTRMOD_tank_water_model[] = {
    gsSPTexture(0, 0, 0, G_TX_RENDERTILE, G_OFF),
    gsDPPipeSync(),
    gsDPSetCombineLERP(0, 0, 0, SHADE, 0, 0, 0, SHADE, 0, 0, 0, SHADE, 0, 0, 0, SHADE),
    gsDPSetRenderMode(G_RM_XLU_SURF, G_RM_XLU_SURF2),
    gsSPLoadGeometryMode(G_ZBUFFER | G_SHADE | G_FOG | G_SHADING_SMOOTH | G_CULL_BACK),
    gsSPVertex(aFTRMOD_tank_water_v, 8, 0),
    /* top, front, back, left, right faces (outward winding) */
    gsSPNTrianglesInit_5b(10, 0, 2, 1, 0, 3, 2, 3, 6, 2),
    gsSPNTriangles_5b(3, 7, 6, 4, 1, 5, 4, 0, 1, 4, 3, 0),
    gsSPNTriangles_5b(4, 7, 3, 5, 2, 6, 5, 1, 2, 0, 0, 0),
    gsSPEndDisplayList(),
};

/* --- draw proc ------------------------------------------------------------ */

static void aFTRMOD_fish_tank_draw(FTR_ACTOR* ftr_actor, ACTOR* my_room, GAME* game, u8* bank) {
    static int swim_frame_ptn[8] = { 0, 0, 1, 1, 2, 2, 1, 1 };

    int fish_idx = FISH_NUM_VANILLA + (ftr_actor->name - FTR_MOD_FISH00);
    int gyo_type = aGYO_FISH_IDX_2_TYPE(fish_idx);
    GRAPH* graph = game->graph;
    aGYO_DL_c* fish_dl;
    int t;
    int phase;
    f32 sway;
    f32 bob;
    s16 heading;
    Gfx* frame_dl;

    if (gyo_type < 0 || gyo_type >= aGYO_TYPE_MODDED_NUM) {
        return;
    }

    fish_dl = aGYO_displayList[gyo_type];

    /* swim animation: triangle-wave glide with a flip at each end + slight bob */
    t = game->frame_counter + (ftr_actor->id * 64);
    phase = t & 0x1FF; /* 512-frame loop */

    if (phase < 256) {
        sway = ((f32)phase - 128.0f) * (1.0f / 128.0f);
        heading = 0x4000; /* +X */
    } else {
        sway = (384.0f - (f32)phase) * (1.0f / 128.0f);
        heading = -0x4000; /* -X */
    }

    bob = ((t & 0x3F) < 32 ? (f32)(t & 0x3F) : (f32)(64 - (t & 0x3F))) * 0.045f;

    if (fish_dl != NULL) {
        Matrix_push();
        Matrix_translate(sway * 7.0f, 12.0f + bob, 0.0f, MTX_MULT);
        Matrix_RotateY(heading, MTX_MULT);
        Matrix_scale(0.02f, 0.02f, 0.02f, MTX_MULT);

        frame_dl = ((Gfx**)fish_dl)[swim_frame_ptn[(t >> 2) & 7]];

        OPEN_DISP(graph);
        gSPMatrix(NEXT_POLY_OPA_DISP, _Matrix_to_Mtx_new(graph), G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
        gSPDisplayList(NEXT_POLY_OPA_DISP, frame_dl);
        CLOSE_DISP(graph);

        Matrix_pull();
    }

    /* tank around the fish (base opaque, water translucent) */
    OPEN_DISP(graph);
    gSPMatrix(NEXT_POLY_OPA_DISP, _Matrix_to_Mtx_new(graph), G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
    gSPDisplayList(NEXT_POLY_OPA_DISP, aFTRMOD_tank_base_model);
    gSPMatrix(NEXT_POLY_XLU_DISP, _Matrix_to_Mtx_new(graph), G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
    gSPDisplayList(NEXT_POLY_XLU_DISP, aFTRMOD_tank_water_model);
    CLOSE_DISP(graph);
}

static aFTR_vtable_c aFTRMOD_fish_tank_vtable = {
    NULL, /* ct */
    NULL, /* move */
    &aFTRMOD_fish_tank_draw,
    NULL, /* dt */
    NULL, /* dma */
};

aFTR_PROFILE iam_mod_fish00 = {
    NULL, /* opaque0 */
    NULL, /* opaque1 */
    NULL, /* translucent0 */
    NULL, /* translucent1 */
    NULL, /* texture */
    NULL, /* palette */
    NULL, /* rig */
    NULL, /* tex_anim */
    26.0f, /* height */
    1.0f,  /* scale (draw proc works in world units) */
    aFTR_SHAPE_TYPEA, /* 1x1 */
    mCoBG_FTR_TYPEA,
    0,
    2,
    0,
    aFTR_INTERACTION_FISH,
    &aFTRMOD_fish_tank_vtable,
};
