unsigned char itemName_paper[] = {
#include "assets/itemName_paper.inc"
};

unsigned char itemName_money[] = {
#include "assets/itemName_money.inc"
};

unsigned char itemName_tool[] = {
#include "assets/itemName_tool.inc"
};

unsigned char itemName_fish[] = {
#include "assets/itemName_fish.inc"
    /* modded fish names: 16 bytes each, space padded (see fish/ADDING_FISH.md) */
    'n', 'e', 'o', 'n', ' ', 't', 'e', 't', 'r', 'a', ' ', ' ', ' ', ' ', ' ', ' ', /* neon tetra */
    'p', 'i', 'k', 'e', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* pike */
    'y', 'e', 'l', 'l', 'o', 'w', ' ', 'p', 'e', 'r', 'c', 'h', ' ', ' ', ' ', ' ', /* yellow perch */
    's', 't', 'u', 'r', 'g', 'e', 'o', 'n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* sturgeon */
    'g', 'o', 'l', 'd', 'e', 'n', ' ', 't', 'r', 'o', 'u', 't', ' ', ' ', ' ', ' ', /* golden trout */
    't', 'i', 'l', 'a', 'p', 'i', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* tilapia */
    'b', 'e', 't', 't', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* betta */
    'r', 'a', 'i', 'n', 'b', 'o', 'w', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', ' ', /* rainbowfish */
    'g', 'a', 'r', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* gar */
    'd', 'o', 'r', 'a', 'd', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* dorado */
    's', 'a', 'd', 'd', 'l', 'e', 'd', ' ', 'b', 'i', 'c', 'h', 'i', 'r', ' ', ' ', /* saddled bichir */
    'n', 'i', 'b', 'b', 'l', 'e', ' ', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', ' ', /* nibble fish */
    't', 'a', 'd', 'p', 'o', 'l', 'e', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* tadpole */
    's', 'n', 'a', 'p', 'p', 'i', 'n', 'g', ' ', 't', 'u', 'r', 't', 'l', 'e', ' ', /* snapping turtle */
    's', 'o', 'f', 't', 's', 'h', 'e', 'l', 'l', ' ', 't', 'u', 'r', 't', 'l', 'e', /* softshell turtle */
    'm', 'i', 't', 't', 'e', 'n', ' ', 'c', 'r', 'a', 'b', ' ', ' ', ' ', ' ', ' ', /* mitten crab */
    't', 'u', 'n', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* tuna */
    'b', 'l', 'u', 'e', ' ', 'm', 'a', 'r', 'l', 'i', 'n', ' ', ' ', ' ', ' ', ' ', /* blue marlin */
    'o', 'c', 'e', 'a', 'n', ' ', 's', 'u', 'n', 'f', 'i', 's', 'h', ' ', ' ', ' ', /* ocean sunfish */
    'r', 'a', 'y', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* ray */
    's', 'a', 'w', ' ', 's', 'h', 'a', 'r', 'k', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* saw shark */
    'h', 'a', 'm', 'm', 'e', 'r', 'h', 'e', 'a', 'd', ' ', 's', 'h', 'a', 'r', 'k', /* hammerhead shark */
    'g', 't', '.', ' ', 'w', 'h', 'i', 't', 'e', ' ', 's', 'h', 'a', 'r', 'k', ' ', /* gt. white shark */
    'w', 'h', 'a', 'l', 'e', ' ', 's', 'h', 'a', 'r', 'k', ' ', ' ', ' ', ' ', ' ', /* whale shark */
    'n', 'a', 'p', 'o', 'l', 'e', 'o', 'n', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', /* napoleonfish */
    'b', 'a', 'r', 'r', 'e', 'l', 'e', 'y', 'e', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* barreleye */
    'm', 'a', 'h', 'i', '-', 'm', 'a', 'h', 'i', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* mahi-mahi */
    'r', 'i', 'b', 'b', 'o', 'n', ' ', 'e', 'e', 'l', ' ', ' ', ' ', ' ', ' ', ' ', /* ribbon eel */
    'm', 'o', 'r', 'a', 'y', ' ', 'e', 'e', 'l', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* moray eel */
    's', 'e', 'a', 'h', 'o', 'r', 's', 'e', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* seahorse */
    'c', 'l', 'o', 'w', 'n', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* clownfish */
    's', 'u', 'r', 'g', 'e', 'o', 'n', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', ' ', /* surgeonfish */
    'b', 'u', 't', 't', 'e', 'r', 'f', 'l', 'y', ' ', 'f', 'i', 's', 'h', ' ', ' ', /* butterfly fish */
    'z', 'e', 'b', 'r', 'a', ' ', 't', 'u', 'r', 'k', 'e', 'y', 'f', 'i', 's', 'h', /* zebra turkeyfish */
    'p', 'u', 'f', 'f', 'e', 'r', ' ', 'f', 'i', 's', 'h', ' ', ' ', ' ', ' ', ' ', /* puffer fish */
    'h', 'o', 'r', 's', 'e', ' ', 'm', 'a', 'c', 'k', 'e', 'r', 'e', 'l', ' ', ' ', /* horse mackerel */
    's', 'q', 'u', 'i', 'd', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* squid */
    'a', 'n', 'c', 'h', 'o', 'v', 'y', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', /* anchovy */
    'f', 'o', 'o', 't', 'b', 'a', 'l', 'l', ' ', 'f', 'i', 's', 'h', ' ', ' ', ' ', /* football fish */
    'o', 'l', 'i', 'v', 'e', ' ', 'f', 'l', 'o', 'u', 'n', 'd', 'e', 'r', ' ', ' ', /* olive flounder */
};

unsigned char itemName_cloth[] = {
#include "assets/itemName_cloth.inc"
};

unsigned char itemName_etc[] = {
#include "assets/itemName_etc.inc"
};

unsigned char itemName_carpet[] = {
#include "assets/itemName_carpet.inc"
};

unsigned char itemName_wall[] = {
#include "assets/itemName_wall.inc"
};

unsigned char itemName_fruit[] = {
#include "assets/itemName_fruit.inc"
};

unsigned char itemName_plant[] = {
#include "assets/itemName_plant.inc"
};

unsigned char itemName_minidisk[] = {
#include "assets/itemName_minidisk.inc"
};

unsigned char itemName_dummy[] = {
#include "assets/itemName_dummy.inc"
};

unsigned char itemName_ticket[] = {
#include "assets/itemName_ticket.inc"
};

unsigned char itemName_insect[] = {
#include "assets/itemName_insect.inc"
};

unsigned char itemName_hukubukuro[] = {
#include "assets/itemName_hukubukuro.inc"
};

unsigned char itemName_kabu[] = {
#include "assets/itemName_kabu.inc"
};

unsigned char ftrName_table[] = {
#include "assets/ftrName_table.inc"
};

unsigned char ftrName2_table[] = {
#include "assets/ftrName2_table.inc"
};
