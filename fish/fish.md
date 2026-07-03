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
| 42 | Pike | 1,800 Bells | Large (L) | River | All day | ––––––––SOND | modded |
| 43 | Yellow perch | 300 Bells | Medium (M) | River | All day | JFM––––––OND | modded |
| 44 | Sturgeon | 10,000 Bells | Very Large (XL) | River (mouth) | All day | JFM–––––SOND | modded |
| 45 | Golden trout | 15,000 Bells | Medium (M) | Waterfall | 4 AM – 9 AM; 4 PM – 9 PM | ––MAM–––SON– | modded |
| 46 | Tilapia | 800 Bells | Medium (M) | River | All day | –––––JJAS––– | modded |
| 47 | Betta | 2,500 Bells | Small (XS) | River | 4 AM – 9 PM | ––––MJJASO–– | modded |
| 48 | Rainbowfish | 800 Bells | Tiny (XXS) | River | 4 AM – 9 PM | ––––MJJASO–– | modded |
| 49 | Gar | 6,000 Bells | Very Large (XL) | Pond | All day | –––––JJAS––– | modded |
| 50 | Dorado | 15,000 Bells | Large (L) | River | 4 AM – 9 PM | –––––JJAS––– | modded |
| 51 | Saddled bichir | 4,000 Bells | Medium (M) | River | 4 PM – 9 AM | –––––JJAS––– | modded |
| 52 | Nibble fish | 1,500 Bells | Tiny (XXS) | River | 4 AM – 9 PM | ––––MJJAS––– | modded |
| 53 | Tadpole | 100 Bells | Tiny (XXS) | Pond | All day | –––AMJJ––––– | modded |
| 54 | Snapping turtle | 5,000 Bells | Very Large (XL) | River | 9 PM – 4 AM | –––––––AS––– | modded |
| 55 | Softshell turtle | 3,750 Bells | Large (L) | River | 4 AM – 9 AM; 4 PM – 9 PM | –––––––AS––– | modded |
| 56 | Mitten crab | 2,000 Bells | Small (XS) | River | 4 PM – 9 AM | ––––––––SON– | modded |
| 57 | Tuna | 7,000 Bells | Very Large (XL) | Sea | All day | JFMA––––––ND | modded |
| 58 | Blue marlin | 10,000 Bells | Very Large (XL) | Sea | All day | JFMA––JAS–ND | modded |
| 59 | Ocean sunfish | 4,000 Bells | Huge (XXL) | Sea | All day | ––––––JAS––– | modded |
| 60 | Ray | 3,000 Bells | Very Large (XL) | Sea | All day | –––––––ASON– | modded |
| 61 | Saw shark | 12,000 Bells | Very Large (XL) | Sea | All day | –––––JJAS––– | modded |
| 62 | Hammerhead shark | 8,000 Bells | Very Large (XL) | Sea | All day | –––––JJAS––– | modded |
| 63 | Great white shark | 15,000 Bells | Huge (XXL) | Sea | All day | –––––JJAS––– | modded |
| 64 | Whale shark | 13,000 Bells | Huge (XXL) | Sea | All day | –––––JJAS––– | modded |
| 65 | Napoleonfish | 10,000 Bells | Huge (XXL) | Sea | All day | ––––––JA–––– | modded |
| 66 | Barreleye | 15,000 Bells | Small (XS) | Sea | All day | JFMAMJJASOND | modded |
| 67 | Mahi-mahi | 6,000 Bells | Large (L) | Sea | All day | ––––MJJASO–– | modded |
| 68 | Ribbon eel | 600 Bells | Small-Med (S) | Sea | All day | –––––JJASO–– | modded |
| 69 | Moray eel | 2,000 Bells | Medium (M) | Sea | All day | –––––––ASO–– | modded |
| 70 | Seahorse | 1,100 Bells | Tiny (XXS) | Sea | All day | –––AMJJASO–– | modded |
| 71 | Clownfish | 650 Bells | Tiny (XXS) | Sea | All day | –––AMJJASO–– | modded |
| 72 | Surgeonfish | 1,000 Bells | Small (XS) | Sea | All day | –––AMJJASO–– | modded |
| 73 | Butterfly fish | 1,000 Bells | Small (XS) | Sea | All day | –––AMJJASO–– | modded |
| 74 | Zebra turkeyfish | 500 Bells | Small-Med (S) | Sea | All day | –––AMJJASO–– | modded |
| 75 | Puffer fish | 250 Bells | Small-Med (S) | Sea | All day | ––––––JAS––– | modded |
| 76 | Horse mackerel | 150 Bells | Small (XS) | Sea | All day | JFMAMJJASOND | modded |
| 77 | Squid | 500 Bells | Small-Med (S) | Sea | All day | JFMAMJJA–––D | modded |
| 78 | Anchovy | 200 Bells | Tiny (XXS) | Sea | All day | JFMAMJJASOND | modded |
| 79 | Football fish | 2,500 Bells | Large (L) | Sea | All day | JFM–––––––ND | modded |
| 80 | Olive flounder | 800 Bells | Large (L) | Sea | All day | JFMAMJJASOND | modded |
