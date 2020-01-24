# pkmn-route-rando
A key item/warp randomizer for Pokemon Red and Blue, in development.

CURRENTLY MAPPING OUT LOGIC: up to Route 4 past Mt. Moon

## HOW TO USE
don't. it doesn't even do anything with any roms yet

## IMPLEMENTED
- A solver that can attempt to go from point A to point B with a set starting inventory, picking up items along the way
- An algorithm for finding "bridges" in the map, useful for making sure the player can't find their way to the other side of one-way obstacles

## Logic Changes From Base Game
- Path between Viridian City and Route 2 is blocked until the Pokedex is acquired (originally just from VC to R2)
- Path between Pewter City and Route 3 is blocked until the Boulder Badge is acquired (originally just from PC to R3)
- You can no longer hop down a ledge to get back to Pewter City after leaving the backside of the Pewter Museum
- You can return to Mt. Moon from Cerulean City along Route 4

## Things To Keep In Mind
- If key items are shuffled with hidden items, you will always be able to get the Itemfinder before picking up any hidden items

## Things to Implement Later
- First is key item shuffling
- An option to start right in Oak's Lab, allowing Red's House to be shuffled with the Pokemon Centers
- An option to skip the Oak's Parcel sidequest (it and its location will be removed from the pools)
  - Both options above allow Oak's Lab to be shuffled
- An option to allow HMs to be used regardless of badges you have obtained
- An "I Know Where Hidden Items Are" option that removes the Itemfinder requirement from hidden item logic
- Fill out this README more, and better
