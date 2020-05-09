# pkmn-route-rando
A key item/warp randomizer for Pokemon Red and Blue, in development.

Inspired by stump's Pokémon Red/Blue Key Item Randomizer: https://github.com/stump/keyrand
(pieces of the patcher code were shamelessly lifted from there)

CURRENTLY MAPPING OUT LOGIC: up to S.S. Anne

## HOW TO USE
Don't. It doesn't even randomize everything yet. You can currently, however, run "patcher.py [rom filname] [flags]" to implement some map changes and randomize items and warps up to Vermillion City and the S.S. Anne. There is no completion logic applied here yet, however. **The program only accepts unaltered UE region Pokemon Red or Blue games!**

### Flags
- **--items [item flags]** - Shuffles items. Item flags are lists of characters separated by spaces. Invalid flags are ignored unless they make Python yell at you or something. See the Wiki for more details.
  - **K** - Shuffles all Key Items.
  - **N** - Shuffles non-key items received from NPCs.
  - **I** - Shuffles item ball pickups.
  - **H** - Shuffles hidden items.
  - For example, using "K I" in your flag set will shuffle Key Items with other Key Items, item ball pickups with other item balls, and leave NPC items and hidden items alone. "KN IH" will shuffle Key Items and NPC items together and item balls and hidden items together, and "K N I H" will shuffle everything in its own pool, and "KNIH" will shuffle all four pools in one large pool.
  - If you already use a flag in one pool and try to put it in another, it will be ignored. Only the first occurrence of each flag counts.
- **--warps** - Shuffles warps.
- **--dungeons** - Breaks up most dungeon and multi-floor buildings when shuffling warps. Does nothing if --warps is not active.

## IMPLEMENTED
- A solver that can attempt to go from point A to point B with a set starting inventory, picking up items along the way
- An algorithm for finding "bridges" in the map, useful for making sure the player can't find their way to the other side of one-way obstacles
- Shuffling and mixing of various item pools
- Warp shuffling
- No logic has been connected yet to either shuffles, with the exception of making sure all locations are physically connected in one group and each town has direct access to exactly one Pokemon Center
- Writing patches to a ROM file, including logic fixes and behind-the-scenes fixes to make the replacements work properly

## Logic Changes From Base Game (these are actually implemented in the patcher)
- Path between Viridian City and Route 2 is blocked until the Pokedex is acquired (originally just from VC to R2)
  - Viridian Gym is on the Route 2 side of this obstacle, and the ledge below it has been turned into trees
  - Cut can also be used to bypass the old man
- Path between Pewter City and Route 3 is blocked until the Boulder Badge is acquired (originally just from PC to R3)
- You can no longer hop down a ledge to get back to Pewter City after leaving the backside of the Pewter Museum
- You can return to Mt. Moon from Cerulean City along Route 4
- You can no longer use the ledge to the right side of Cerulean Gym to return to the main area of the city from the outside. You must use the Cuttable tree or find another way in
- Both fossils can be obtained from Mt. Moon

## Things To Keep In Mind
- Every town has direct access to exactly one Pokemon Center
  - The Mt. Moon and Rock Tunnel Pokemon Centers are left as is...for now
  - This does NOT apply to PokeMarts

## Things To Keep In Mind That Don't Actually Apply Yet
- Flash is available before you have to traverse Rock Tunnel
- If key items are shuffled with hidden items, you will always be able to get the Itemfinder before picking up any hidden items
- The back entrances of Pokemon Mansion and the Power Plant lead back to wherever the regular entrance leads
- Mr. Fuji teleports the player to wherever the entrance of Pokemon Tower is instead of his house. You still have to find him again and talk to him to get the Poke Flute
  - If dungeon areas are disconnected, Mr. Fuji will not teleport the player at all
- Nothing past the entrance to Route 23 is shuffled (though the entrance itself is), meaning the Victory Road and Indigo Plateau are left intact
  - The order of the Elite Four are shuffled, however. Champion is still last
- Safari Zone is left intact

## Things to Implement Later
- An option to start right in Oak's Lab, allowing Red's House to be shuffled as a Pokemon Center, and Oak's Lab to be shuffled in general
- An option to skip the Oak's Parcel sidequest (it and its location will be removed from the pools)
- An option to allow HMs to be used regardless of badges you have obtained
- An "I Know Where Hidden Items Are" option that removes the Itemfinder requirement from hidden item logic
- Fill out this README more, and better
