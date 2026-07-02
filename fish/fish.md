# Fish (generated from game code — do not hand-edit)

Regenerate with: `python fish/gen_fish_table.py --write`

Sources: `src/actor/ac_set_ovl_gyoei.c` (spawns), `src/data/item/fish_price.c`
(sell = catalog price / 4), `src/actor/ac_gyoei_type.c_inc` (shadow sizes),
`src/game/m_inventory_ovl.c` (encyclopedia order).

Time slots are the game's four spawn windows: 9 PM–4 AM, 4–9 AM, 9 AM–4 PM, 4–9 PM.
Months: letter = available that month (spawn tables are per half-month; both halves merged).
Notes: `island` = also spawns at the island, `tourney` = boosted during the fishing tourney.

## Page 1

| # | Name | Sell price | Shadow size | Location | Time | Months | Notes |
|---|------|-----------|-------------|----------|------|--------|-------|
| 1 | Crucian carp | 120 Bells | Small (XS) | River | All day | JFMAMJJASOND |  |
| 2 | Brook trout | 150 Bells | Small-Med (S) | River (pool) | All day | JFMAMJJASOND |  |
| 3 | Carp | 300 Bells | Large (L) | River | All day | JFMAMJJASOND |  |
| 4 | Koi | 2,000 Bells | Large (L) | River | 4 PM – 9 AM | JFMAMJJASOND |  |
| 5 | Barbel steed | 200 Bells | Large (L) | River | All day | JFMAMJJASOND |  |
| 6 | Dace | 200 Bells | Medium (M) | River | 4 PM – 9 AM | JFMAMJJASOND |  |
| 7 | Catfish | 200 Bells | Large (L) | River | 4 PM – 9 AM | ––––MJJASO–– |  |
| 8 | Giant catfish | 3,000 Bells | Very Large (XL) | River (pool) | 4 PM – 9 AM | –––––JJA–––– |  |
| 9 | Pale chub | 200 Bells | Small (XS) | River | 9 AM – 4 PM | JFMAMJJASOND |  |
| 10 | Bitterling | 1,300 Bells | Tiny (XXS) | River | All day | JF–––––––––D |  |
| 11 | Loach | 300 Bells | Tiny (XXS) | River | All day | ––MAM––––––– |  |
| 12 | Bluegill | 120 Bells | Small (XS) | River | 9 AM – 4 PM | JFMAMJJASOND |  |
| 13 | Small bass | 200 Bells | Small (XS) | River | All day | JFMAMJJASOND | tourney |
| 14 | Bass | 300 Bells | Medium (M) | River | All day | JFMAMJJASOND | tourney |
| 15 | Large bass | 3,000 Bells | Large (L) | River | All day | JFMAMJJASOND | tourney |
| 16 | Giant snakehead | 6,500 Bells | Very Large (XL) | River (pool) | 9 AM – 4 PM | –––––JJA–––– |  |
| 17 | Eel | 2,000 Bells | Small-Med (S) | River | 4 PM – 9 AM | –––––JJAS––– |  |
| 18 | Freshwater goby | 300 Bells | Small (XS) | River | All day | JFMAMJJASOND |  |
| 19 | Pond smelt | 300 Bells | Tiny (XXS) | River | All day | JF–––––––––D |  |
| 20 | Sweetfish | 1,300 Bells | Small (XS) | River | All day | ––––––JAS––– |  |
| 21 | Cherry salmon | 1,300 Bells | Small (XS) | River | 4 AM – 9 AM; 4 PM – 9 PM | ––MAMJ––SON– |  |
| 22 | Rainbow trout | 650 Bells | Medium (M) | River | 4 AM – 9 AM; 4 PM – 9 PM | ––MAMJ––SON– |  |
| 23 | Large char | 10,000 Bells | Large (L) | Waterfall | 4 AM – 9 AM; 4 PM – 9 PM | ––MAMJ––SON– |  |
| 24 | Stringfish | 15,000 Bells | Very Large (XL) | River | 4 PM – 9 AM | JF–––––––––D |  |
| 25 | Salmon | 650 Bells | Large (L) | River, River (mouth) | All day | ––––––––S––– |  |
| 26 | Goldfish | 1,300 Bells | Tiny (XXS) | River | All day | JFMAMJJASOND |  |
| 27 | Popeyed goldfish | 1,300 Bells | Tiny (XXS) | River | 9 AM – 4 PM | JFMAMJJASOND |  |
| 28 | Guppy | 1,300 Bells | Tiny (XXS) | River | 9 AM – 4 PM | –––AMJJASON– |  |
| 29 | Angelfish | 3,000 Bells | Small (XS) | River | 4 PM – 9 AM | ––––MJJASO–– |  |
| 30 | Piranha | 6,500 Bells | Small (XS) | River | 9 AM – 4 PM; 9 PM – 4 AM | –––––JJAS––– |  |
| 31 | Arowana | 10,000 Bells | Medium (M) | River | 4 AM – 9 AM; 4 PM – 9 PM | –––––JJAS––– |  |
| 32 | Coelacanth | 15,000 Bells | Very Large (XL) | Sea (raining) | 4 PM – 9 AM | JFMAMJJASOND |  |
| 33 | Crawfish | 250 Bells | Small (XS) | Pond | All day | –––AMJJAS––– |  |
| 34 | Frog | 250 Bells | Tiny (XXS) | Pond | All day | ––––MJJA–––– |  |
| 35 | Killifish | 300 Bells | Tiny (XXS) | Pond, River | All day | –––AMJJA–––– |  |
| 36 | Jellyfish | 100 Bells | Medium (M) | Sea | All day | –––––––A–––– |  |
| 37 | Sea bass | 120 Bells | Large (L) | Sea | All day | JFMAMJJASOND | island |
| 38 | Red snapper | 3,000 Bells | Large (L) | Sea | All day | JFMAMJJASOND | island |
| 39 | Barred knifejaw | 5,000 Bells | Large (L) | Sea | All day | ––MAMJJASON– | island |
| 40 | Arapaima | 10,000 Bells | Huge (XXL) | River | 4 PM – 9 AM | ––––––JAS––– |  |

## Page 2 (new fish)

| # | Name | Sell price | Shadow size | Location | Time | Months | Notes |
|---|------|-----------|-------------|----------|------|--------|-------|
| 41 | Neon tetra | 2,000 Bells | Tiny (XXS) | River | 9 PM – 4 AM | –––––JJAS––– | modded |
| 42 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 43 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 44 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 45 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 46 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 47 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 48 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 49 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 50 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 51 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 52 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 53 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 54 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 55 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 56 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 57 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 58 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 59 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 60 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 61 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 62 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 63 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 64 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 65 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 66 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 67 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 68 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 69 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 70 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 71 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 72 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 73 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 74 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 75 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 76 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 77 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 78 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 79 | *(empty slot)* | — | — | — | — | –––––––––––– | |
| 80 | *(empty slot)* | — | — | — | — | –––––––––––– | |
