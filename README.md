# pkmn-route-rando
A key item/warp randomizer for Pokemon Red and Blue, in development.

Inspired by stump's Pokémon Red/Blue Key Item Randomizer: https://github.com/stump/keyrand
(pieces of the patcher code were shamelessly lifted from there)

CURRENTLY MAPPING OUT LOGIC: up to Route 4 past Mt. Moon

## HOW TO USE
Don't. It doesn't even randomize everything yet. You can currently, however, run "patcher.py [rom filname]" to implement some map changes and randomize _all_ items up until Route 4. There is no logic applied here yet, however. Flags to toggle/separate the pools to be added later. **The program only accepts unaltered UE region Pokemon Red or Blue games!**

## IMPLEMENTED
- A solver that can attempt to go from point A to point B with a set starting inventory, picking up items along the way
- An algorithm for finding "bridges" in the map, useful for making sure the player can't find their way to the other side of one-way obstacles
- Shuffling and mixing of various item pools
- Writing patches to a ROM file, including logic fixes and behind-the-scenes fixes to make the replacements work properly

## Logic Changes From Base Game (these are actually implemented in the patcher)
- Path between Viridian City and Route 2 is blocked until the Pokedex is acquired (originally just from VC to R2)
  - Viridian Gym is on the Route 2 side of this obstacle, and the ledge below it has been turned into trees
  - Cut can also be used to bypass the old man
- Path between Pewter City and Route 3 is blocked until the Boulder Badge is acquired (originally just from PC to R3)
- You can no longer hop down a ledge to get back to Pewter City after leaving the backside of the Pewter Museum
- You can return to Mt. Moon from Cerulean City along Route 4
- You can no longer use the ledge to the right side of Cerulean Gym to return to the main area of the city from the outside. You must use the Cuttable tree or find another way in

## Things To Keep In Mind (none of this actually applies yet)
- Every town has direct access to exactly one Pokemon Center
  - The Mt. Moon and Rock Tunnel Pokemon Centers are left as is...for now
  - This does NOT apply to PokeMarts
- Both fossils can be obtained from Mt. Moon
- Flash is available before you have to traverse Rock Tunnel
- If key items are shuffled with hidden items, you will always be able to get the Itemfinder before picking up any hidden items
- The back entrances of Pokemon Mansion and the Power Plant lead back to wherever the regular entrance leads
- Mr. Fuji teleports the player to wherever the entrance of Pokemon Tower is instead of his house. You still have to find him again and talk to him to get the Poke Flute
  - If dungeon areas are disconnected, Mr. Fuji will not teleport the player at all
- Nothing past the entrance to Route 23 is shuffled (though the entrance itself is), meaning the Victory Road and Indigo Plateau are left intact
  - The order of the Elite Four are shuffled, however. Champion is still last
- Safari Zone is left intact

## Things to Implement Later
- First is key item shuffling
- An option to start right in Oak's Lab, allowing Red's House to be shuffled with the Pokemon Centers
- An option to skip the Oak's Parcel sidequest (it and its location will be removed from the pools)
  - Both options above allow Oak's Lab to be shuffled
- An option to allow HMs to be used regardless of badges you have obtained
- An "I Know Where Hidden Items Are" option that removes the Itemfinder requirement from hidden item logic
- Fill out this README more, and better
