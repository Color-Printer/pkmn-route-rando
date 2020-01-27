import binascii
from game_data import *
import argparse

class UnrecognizedROM(Exception):
    pass

version = ""

def replace(rom, addr, hex):
    # hey did you know the credits saying "BLUE" instead of "RED" shifts
    # everything below it in bank 1D forward in address by one byte?????
    if version == "blue" and (addr >= 0x74347 and addr <= 0x7867A):
        addr+=1
    bin = binascii.unhexlify(hex)
    rom[addr:addr+len(bin)] = bin

def replace_item(rom, addr, item):
    if version == "blue" and (addr >= 0x74347 and addr <= 0x7867A):
            addr+=1
    rom[addr] = item.id

parser = argparse.ArgumentParser(description='A key item/warp randomizer for Pokemon Red and Blue.')
parser.add_argument('romfile', type=argparse.FileType('rb'), help="filename for a valid Pokemon Red or Blue UE ROM.")
args = parser.parse_args()

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

# create a gap in a ledge on route 4 to allow access to mt. moon from
# cerulean city.
replace(romData,0x544C7,"5C")

# replace a ledge with a fence to prevent hopping back into cerulean city
# from the outside, forcing the player to use the Cut tree to the south or
# finding another way in.
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
# Make Mr. Fuji not be required by changing the initial state of the Silph guards.
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
# dream eater guy in viridian city
replace(romData, 0x191D0, '995423')

key_items = game.shuffle_items()

for old, new in key_items.items():
    replace_item(romData,old.address,new.item)

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