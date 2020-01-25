import binascii

def replace(rom, addr, hex):
    bin = binascii.unhexlify(hex)
    rom[addr:addr+len(bin)] = bin

# open and read the rom file
romFile = open("pkmnred.gb","rb")
romData = memoryview(bytearray(romFile.read()))
romFile.close()

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

# replace the ledge to the south of the pewter museum back entrance with a
# row of trees to prevent not being able to go back in.
replace(romData,0x1862B,"1C6F6F6F0F")

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

# fix the header checksum
romData[0x0014e:0x00150] = b'\0\0'
checksum = sum(romData) & 0xffff
romData[0x0014e] = checksum >> 8
romData[0x0014f] = checksum & 0xff

#write the data to a new file
newRom = open("pkmnred_rando.gb","wb")
newRom.write(romData)
newRom.close()
