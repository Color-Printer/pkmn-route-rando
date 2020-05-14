import binascii
from game_data import *
import argparse
import random

class UnrecognizedROM(Exception):
    pass

class GenerationError(Exception):
    pass

version = ""

def addressShift(addr):
    if version == "blue" and (addr >= 0x74347 and addr <= 0x7867A):
        return addr+1
    else:
        return addr

def replace(rom, addr, hex):
    # hey did you know the credits saying "BLUE" instead of "RED" shifts
    # everything below it in bank 1D forward in address by one byte?????
    addr = addressShift(addr)
    bin = binascii.unhexlify(hex)
    rom[addr:addr+len(bin)] = bin

def replace_item(rom, addr, item):
    addr = addressShift(addr)
    rom[addr] = item.id

def replace_warp(rom, w_a, w_b):
    warp_a = game.areas[w_a[0]].exits[w_a[3]]
    warp_b = game.areas[w_b[0]].exits[w_b[3]]
    map_a_addr = addressShift(game.areas[warp_a.home].warpAddresses)
    map_b_addr = addressShift(game.areas[warp_b.home].warpAddresses)
    map_a_offset = map_a_addr + (4 * warp_a.warp_id)
    map_b_offset = map_b_addr + (4 * warp_b.warp_id)
    rom[map_a_offset+2] = warp_b.warp_id
    rom[map_a_offset+3] =  game.areas[warp_b.home].mapid
    rom[map_b_offset+2] = warp_a.warp_id
    rom[map_b_offset+3] =  game.areas[warp_a.home].mapid
    for x in warp_a.extra_warp_id:
        map_a_offset = map_a_addr + (4 * x)
        rom[map_a_offset+2] = warp_b.warp_id
        rom[map_a_offset+3] =  game.areas[warp_b.home].mapid
    for x in warp_b.extra_warp_id:
        map_b_offset = map_b_addr + (4 * x)
        rom[map_b_offset+2] = warp_a.warp_id
        rom[map_b_offset+3] =  game.areas[warp_a.home].mapid


parser = argparse.ArgumentParser(description='A key item/warp randomizer for Pokemon Red and Blue.')
parser.add_argument('romfile', type=argparse.FileType('rb'), help="filename for a valid Pokemon Red or Blue UE ROM.")
parser.add_argument('--seed', dest='seed', type=int, help="filename for a valid Pokemon Red or Blue UE ROM.")
parser.add_argument('--items', dest='item_flags', nargs='*', default=["K"], help="Shuffle items into different pools. See documentation for details.")
parser.add_argument('--warps', dest='warps_r', action='store_true', help="Shuffle warps.")
parser.add_argument('--dungeons', dest='dungeons_r', action='store_true', help="Breaks up most dungeon and multi-floor buildings when shuffling warps.")
parser.add_argument('--freehms', dest='freehms', action='store_true', help="Removes badge requirements from HMs.")
parser.add_argument('--knowhidden', dest='knowhidden', action='store_true', help='"I Know Where Hidden Items Are!" Itemfinder not required in logic to find hidden items.')
parser.add_argument('--open', dest='open', action='store_true', help='Enables all the "open" flags.')
parser.add_argument('--openoldman', dest='open_old_man', action='store_true', help='The old man in Viridian City no longer blocks the way.')
parser.add_argument('--opengym8', dest='open_gym8', action='store_true', help='The Viridian Gym entrance no longer requires the first seven badges.')
parser.add_argument('--faststart', dest='faststart', action='store_true', help="The player starts directly in Oak's Lab, ready to pick a starter.")
args = parser.parse_args()

if args.open == True:
    args.open_old_man = True
    args.open_gym8 = True

with args.romfile as romFile:
    romData = memoryview(bytearray(romFile.read()))

if len(romData) != 1048576:
    raise UnrecognizedROM("Invalid ROM size!")

if (romData[0x14E] != 0x91 or romData[0x14F] != 0xE6) and (romData[0x14E] != 0x9D or romData[0x14F] != 0x0A):
    raise UnrecognizedROM("Checksum invalid! Not an original Pokemon Red/Blue UE ROM!")

if romData[0x14E] == 0x91:
    version = "red"
else:
    version = "blue"

r = random.Random(args.seed)

##########################################################################
# First, it's patch time!!!! Let's set up some patches necessary for the #
# randomizer.                                                            #
##########################################################################
# First, skip the check for being next to the old man. We're moving him anyway
# and I actually don't know how to change the coordinate check without screwing
# things up.
replace(romData,0x19005,"C3")
# next, move the old man and girl up one tile.
replace(romData,0x183C1,"0C")
replace(romData,0x183C7,"0C")
# then move the sign object down to be just above them. together, all three
# block the way.
replace(romData,0x1839E,"07")
# now move the actual sign tile.
replace(romData,0x183F5,"01")
replace(romData,0x18431,"08")
# replace the ledge below the viridian gym with trees.
replace(romData,0x18448,"1C1C1C1C1C1C")

# replace the ledge to the south of the pewter museum back entrance with a
# row of trees to prevent not being able to go back in.
replace(romData,0x1862B,"1C6F6F6F0F")
# fix the door pushing you into the trees indefinitely.
# this causes a slightly weird interaction with the old man but it
# Technically Functions so
replace(romData,0x190D8,"10")

# put a fence blocking most of the way between pewter city and route 3,
# lined up with the guy blocking the way.
replace(romData,0x18698,"41")
replace(romData,0x186AC,"4E")
# skip the part where the guy checks to see if you're in front of him.
replace(romData,0x19263,"C9")
# skip the part where he drags you to the gym.
replace(romData,0x1943d,"C3D724")

# allow the player to pick up both fossils on mt moon.
replace(romData,0x49E86,"94")
replace(romData,0x49F5A,"00")

# create a gap in a ledge on route 4 to allow access to mt. moon from
# cerulean city.
replace(romData,0x544C7,"5C")

# replace a ledge with a fence to prevent hopping back into cerulean city
# from the outside, forcing the player to use the Cut tree to the south or
# find another way in.
replace(romData,0x188F4,"777701")

# the following fixes set up key item shuffling properly (mainly text stuff)
# and were shamelessly lifted from stump's key item randomizer (see README).
# Bicycle slot
replace(romData, 0x1d754, 'fc')
replace(romData, 0x1d75c, '2c')
replace(romData, 0x1d783, '78')
# the following also patches the instant text bug
replace(romData, 0x1d787, '18f6211058cd493cafea26ccea2acc3e03ea29cc3e01ea28ccea25cc3cea24cc2130d7cbf621a0c3010f04cd2219cd29243e06ea1ed1cdcf2f21cac3116dcdcd551911ff57cd551921e4c3110758cd5519211558cd493ccdbe3a2130d7cbb6cb4f200cfa26cca72006211a58cd493c212a58cd493cc3d724')
replace(romData, 0x98ed4, '50014bcf00e8505000')

# Bike Voucher slot
replace(romData, 0x59b78, 'c9')
replace(romData, 0x9a83a, '50014bcf00e7505000')

# Coin Case slot
replace(romData, 0x9e086, '50014bcf00e7505000')

# Dome Fossil slot
replace(romData, 0x49e40, '24')
replace(romData, 0x49eef, '3e29cd195f211f5fcd493ccdec35fa26cca7205e010129cd2e3ed2765fcd695f21f6d7cbf63e6dc3515fea1ed1c3cf2f175e492050083e01ea3ccc3e2acd195f')
replace(romData, 0x49f4a, '21f6d7cbfe3e6eea4dcc3e11cd6d3e')
replace(romData, 0x80967, '4f50016dcd00e65700')
replace(romData, 0x8099b, '4f50014bcf00e7505000')

# Good Rod slot
replace(romData, 0xa072d, '50014bcf00e7505000')

# Helix Fossil slot
replace(romData, 0x80982, '4f50016dcd00e65700')

# HM02 slot
replace(romData, 0x1e631, '9954')

# HM05 slot
replace(romData, 0x801a3, '5550015bcc00e7500500')
replace(romData, 0x80244, '5550015bcc00e85700')
replace(romData, 0x802df, '4f50015bcc00e7505000')
replace(romData, 0x80311, '5550015bcc00e85700')

# Old Amber slot
replace(romData, 0x9679c, '50014bcf00e7505000')

# Old Rod slot
replace(romData, 0x9c599, '50014bcf00e7505000')

# Poké Flute slot
# patches the Poké Doll/Marowak oversight.
replace(romData, 0x0d63f, '7664')
replace(romData, 0x0d645, 'c7')
replace(romData, 0x0e022, 'fa5ed3fe93c0fad8cffe91c0213260c9008daee77f93a7a4b1a47fa0b1a44fa4adaeb4a6a77fb2a4b0b4a4ada2a455a1b1a4a0aab27fa8ad7fb3a7a8b255a6a0aca47fa0abb1a4a0a3b87fe355aba4b3bd7fadaeb37fa0a3a355a0adb87facaeb1a4e75850')
replace(romData, 0x0e0c7, 'fa57d03dc28165cd2260cab9')
replace(romData, 0x9a007, '50014bcf00e7505000')

# S.S. Ticket slot
replace(romData, 0x8d4a5, '50014bcf00e7505000')
# the following removes the cerulean guard.
replace(romData, 0x0cb01, '15')
replace(romData, 0x0cb07, '11')

# Super Rod slot
replace(romData, 0x8ca45, '50014bcf00e7505000')

# Tea slot (and implementation)
replace(romData, 0x0476d, 'e6e6e6e6509280858091887f81808b8b50938480')
replace(romData, 0x0d5f1, '7664')
replace(romData, 0x486b2, '8f6312')
replace(romData, 0x4a38f, '08fa78d7cb47280921bd63cd493cc3d72421c263cd493c010109cd2e3e300a2178d7cbc621036418e2217c4a18dd17fe4e27500098aeb47fb2a7aeb4aba3adbe7fb2afa4ada34fa0abab7fb8aeb4b17facaeada4b855aead7fa3b1a8adaab2e85193b1b87fb3a7a8b27fa8adb2b3a4a0a3e8585700527fb1a4a2a4a8b5a4a34f50014bcf00e7501100518daeb3a7a8ada67fa1a4a0b3b24fb3a7a8b1b2b37faba8aaa47fb2aeaca455a7aeb37f938480e85188b37fb1a4a0ababb87fa8b24fb3a7a47fa1a4b2b3e857')
replace_item(romData, 0x4a3a8, TEA)
replace(romData, 0x5a5b7, '090000')

# Town Map slot
replace(romData, 0x94ca2, '4f50014bcf00e7505000')

## the rest of these are mine. thank you stump for making me realize the power
## of wc4fb.
replace(romData, 0x191D0, '995423')
replace(romData, 0x196DF, '995423')
replace(romData, 0x4851C, '995423')
replace(romData, 0x495A2, '995423')
replace(romData, 0x5C4A3, '995423')
replace(romData, 0x5C7CE, '995423')
replace(romData, 0x5D179, '995423')
replace(romData, 0x74AE5, '995423')

# fix the warp code so that it ALWAYS updates your position whenever you use a warp
# by silently changing the current tileset to a dungeon tileset. now overworld to
# overworld warps can function properly.
replace(romData, 0x7B0, 'A63F')
replace(romData, 0x3FA6, 'CDDA123E07EA67D3C9')

# fix rock tunnel not clearing darkness when you leave.
replace(romData, 0x79C, '09')
# fix rock tunnel so both floors get darkness.
replace(romData, 0x75F, 'C3AF3F00')
replace(romData, 0x799, 'C3BF3F00')
replace(romData, 0x3FAF, 'FE522809F08BFEE82803C36B07C36307CB8EF08BFE522809F08BFEE82803C3A607C3AA07')

# fix viridian gym to specifically check the first seven badges. if warps are shuffled,
# the player might get the eighth badge early which would lock them out of the
# viridian gym entrance.
replace(romData, 0x19011, 'C31867')
replace(romData, 0x1A718, 'FA56D3CBBFFE7FC21E50C31850')

# stop s.s. anne from leaving after getting the cut hm
replace(romData, 0x1DB5E, 'C9')

# if free hms are enabled, disables the badge check on using HM moves.
if(args.freehms == True):
    replace(romData, 0x13178, "3EFF00")

# sets the old man to his post-pokedex state if the openoldman flag is enabled.
if(args.open_old_man == True):
    replace(romData, 0xCAEF, "11")
    replace(romData, 0xCAF2, "15")
    replace(romData, 0x19042, "C9")
    replace(romData, 0x19165, "7A")

# opens up the viridian gym if the opengym8 flag is enabled.
if(args.open_gym8 == True):
    replace(romData, 0x19017, "00")
    replace(romData, 0x1911A, "27")

# allows the player to start in oak's lab ready to pick a starter
if(args.faststart == True):
    replace(romData, 0x6420, "282DC70B05010105")
    replace(romData, 0x1CB4E, "214BD7CBFE00")

game = 0
tries = 0

while True:
    tries+=1
    if tries>100000:
        raise UnrecognizedROM("Too many attempts to generate a valid seed!")
    del game
    game = generateGameWorld(r)
    if(args.freehms == True):
        game.inventory.add("free_hms")
    if(args.knowhidden == True):
        game.inventory.add("know_hidden")
    if(args.open_old_man == True):
        game.inventory.add("open_old_man")
    if(args.open_gym8 == True):
        game.inventory.add("open_gym8")
    new_items = game.shuffle_items(args.item_flags)
    if args.warps_r == True:
        new_warps = game.shuffle_warps(args)
    if not game.allPhysicallyConnected():
        print("TRY AGAIN - Not all maps connected!")
        continue
    if not game.checkPokemonCenters():
        print("TRY AGAIN - Every town should have direct access to exactly one Pokemon Center!")
        continue
    break

for old, new in new_items.items():
    replace_item(romData,old.address,new.item)

if args.warps_r == True:
    for a, b in new_warps.items():
        replace_warp(romData,a,b)

# some items ids need to be rewritten again
romData[0x1d7b9]=romData[0x1d765]
romData[0x49f05]=romData[0x49ef0]
romData[0x49f40]=romData[0x49f2b]

# fix the header checksum
romData[0x0014e:0x00150] = b'\0\0'
checksum = sum(romData) & 0xffff
romData[0x0014e] = checksum >> 8
romData[0x0014f] = checksum & 0xff

#write the data to a new file
newRom = open("pkmn"+version+"_rando.gb","wb")
newRom.write(romData)
newRom.close()
