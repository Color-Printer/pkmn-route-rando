from world import *
from items import *

game = World()

##########################################IMPORTANT NOTES##########################################
# - NPCs that will never be randomized *and* don't give items are not listed here.
#   - Examples: Red's Mom, the Old Man while he's blocking the way, etc.
# - Requirements for items from NPCs should be listed under their ItemLocations.
#   - Example: Daisy won't give you the Map unless you have the Pokedex.
# - Requirements for NPCs themselves should be the requirements to actually access the NPC sprite.
#   - Example: The Dream Eater guy in Viridian needs Cut or Surf to reach his location, but you
#     don't need anything to get his item from him.
###################################################################################################

###Pallet Town###
game.newTown("pallet_town","Pallet Town",0x0)
game.newExit("pallet_town","route_1")
#newExit("pallet_town","route_21","canSurf()")
game.newWarp("pallet_town",0,"reds_house_1F",0)
game.newWarp("pallet_town",1,"blues_house",0)
game.newWarp("pallet_town",2,"oaks_lab",1)
game.newNPC("pallet_town",2,"Pallet Girl")
game.newNPC("pallet_town",3,"Technology Dude")

###Red's House###
#1F
game.newArea("reds_house_1F","Red's House - 1F",0x25)
game.newWarp("reds_house_1F",0,"pallet_town",0,"True",[1],[0])
game.newWarp("reds_house_1F",2,"reds_house_2F",0)
#2F
game.newArea("reds_house_2F","Red's House - 2F",0x26)
game.newWarp("reds_house_2F",0,"reds_house_1F",2)

###Blue's House###
game.newArea('blues_house',"Blue's House",0x27)
game.newWarp("blues_house",0,"pallet_town",1,"True",[1],[1])
game.newNPC("blues_house",1,"Daisy Oak",[ItemLocation(TOWN_MAP,"Map Gift","has(POKEDEX)",address=0x19b7c)])
game.key_item_locs.append(game.areas["blues_house"].objects[1].itemsHeld[0])

###Oak's Lab###
game.newArea("oaks_lab","Prof. Oak's Lab",0x28)
game.newWarp("oaks_lab",0,"pallet_town",2,"True",[1],[2])
game.newNPC("oaks_lab",0,"Prof. Oak",[ItemLocation(POKEDEX, "Parcel Exchange","has(OAKS_PARCEL)")])
#Oak will never be randomized (it would just break things too much otherwise), so it's okay
#if he's object number 0
game.newNPC("oaks_lab",7,"Lab Girl")
game.newNPC("oaks_lab",8,"Lab Aide 1")
game.newNPC("oaks_lab",9,"Lab Aide 2")

###Route 1###
game.newArea("route_1","Route 1",0x0C)
game.newExit("route_1","pallet_town")
game.newExit("route_1","viridian_city")
game.newNPC("route_1",1,"Potion Guy",[ItemLocation(POTION,"Free Potion",address=0x1CACA)])
game.npc_item_locs.append(game.areas["route_1"].objects[1].itemsHeld[0])
game.newNPC("route_1",2,"Ledge Dude")

###Viridian City###
#Main Area
game.newTown("viridian_city","Viridian City",0x01)
game.newExit("viridian_city","route_1")
#newExit("viridian_city","route_22")
game.newExit("viridian_city","viridian_north","has(POKEDEX) or canCut()")
game.newWarp("viridian_city",0,"viridian_center",0)
game.newWarp("viridian_city",1,"viridian_mart",0)
game.newWarp("viridian_city",2,"viridian_school",0)
game.newWarp("viridian_city",3,"viridian_house",0)
game.newNPC("viridian_city",1,"Pokeball Kid")
game.newNPC("viridian_city",3,"Caterpillar Kid")
game.newNPC("viridian_city",6,"Dream Eater Guy",[ItemLocation(TM_42,"Dream Eater TM",address=0x191A6)],"canCut() or canSurf()")
game.npc_item_locs.append(game.areas["viridian_city"].objects[6].itemsHeld[0])
game.newNPC("viridian_city",7,"Old Man",req="has(POKEDEX)")
game.newHiddenItem("viridian_city",0,"Hidden Potion on Tree",POTION,address=0x46F8F)
#Above old man
game.newTown("viridian_north","Viridian City - North Part",0x01)
game.newExit("viridian_north","viridian_city","has(POKEDEX) or canCut()")
game.newExit("viridian_north","route_2v")
game.newNPC("viridian_north",2,"Viridian Gym Bystander")
game.newWarp("viridian_north",4,"viridian_gym",0,"firstSevenBadges()")

###Viridian Pokemon Center###
game.newArea("viridian_center","Viridian Pokemon Center",0x29)
game.newWarp("viridian_center",0,"viridian_city",0,"True",[1],[0])
game.newNPC("viridian_center",2,"PC Gentleman")
game.newNPC("viridian_center",3,"Free Healthcare Kid")

###Viridian PokeMart###
game.newArea("viridian_mart","Viridian PokeMart",0x2A)
game.newWarp("viridian_mart",0,"viridian_city",1,"True",[1],[1])
game.newNPC("viridian_mart",0,"Viridian Shopkeeper",[ItemLocation(OAKS_PARCEL,"Parcel Pickup")])
game.newNPC("viridian_mart",2,"Antidote Shopper")
game.newNPC("viridian_mart",3,"Sold-Out Potion Shopper")

###Viridian Schoolhouse###
game.newArea("viridian_school","Viridian Schoolhouse",0x2B)
game.newWarp("viridian_school",0,"viridian_city",2,"True",[1],[2])
game.newNPC("viridian_school",1,"Viridian Student")
game.newNPC("viridian_school",2,"Viridian Teacher")

###Viridian Nickname House###
game.newArea("viridian_house","Viridian Nickname House",0x2C)
game.newWarp("viridian_house",0,"viridian_city",3,"True",[1],[3])
game.newNPC("viridian_house",1,"Viridian Father")
game.newNPC("viridian_house",2,"Viridian Daughter")

###Viridian Gym###
game.newArea("viridian_gym","Viridian Gym",0x2D)
game.newWarp("viridian_gym",0,"viridian_north",4,"True",[1],[4])
game.newNPC("viridian_gym",1,"Giovanni",[ItemLocation(EARTHBADGE,"Giovanni's Badge"),ItemLocation(TM_27,"Giovanni's TM",address=0x749A3)])
game.npc_item_locs.append(game.areas["viridian_gym"].objects[1].itemsHeld[1])
game.newNPC("viridian_gym",10,"Viridian Gym Guide")
game.newItemLoc("viridian_gym",11,"Revive",REVIVE,address=0x74C3E)

###Route 2###
#Viridian Side (south)
game.newArea("route_2v","Route 2 - Viridian Side",0x0D)
game.newExit("route_2v","viridian_city","has(POKEDEX)")
game.newWarp("route_2v",5,"forest_south_gate",2)
game.newExit("route_2v","route_2se","canCut()")
#Southeast Section
game.newArea("route_2se","Route 2 - Southeast Section",0x0D)
game.newExit("route_2se","route_2v","canCut()")
game.newWarp("route_2se",4,"route_2_gate",2)
game.newItemLoc("route_2se",1,"Moon Stone",MOON_STONE,address=0x5404A)
game.newItemLoc("route_2se",2,"HP Up",HP_UP,address=0x54051)
#Mideast Section
game.newArea("route_2m","Route 2 - Mideast Section",0x0D)
game.newExit("route_2m","route_2ne","canCut()")
game.newWarp("route_2m",3,"route_2_gate",1)
#Northeast Section
game.newArea("route_2ne","Route 2 - Northeast Section",0x0D)
game.newExit("route_2ne","route_2m","canCut()")
game.newExit("route_2ne","route_2p","canCut()")
#game.newWarp("route_2ne",0,"diglett_cave_r2",0)
game.newWarp("route_2ne",2,"r2_trade_house",0)
#Pewter Side (north)
game.newArea("route_2p","Route 2 - Pewter Side",0x0D)
game.newExit("route_2p","pewter_city")
game.newExit("route_2p","route_2ne","canCut()")
game.newWarp("route_2p",1,"forest_north_gate",1)

###Route 2 Gate###
game.newArea("route_2_gate","Route 2 Gate",0x31)
game.newWarp("route_2_gate",0,"route_2m",3,"True",[1],[3])
game.newWarp("route_2_gate",2,"route_2se",4,"True",[3],[4])
game.newNPC("route_2_gate",1,"Flash Aide",[ItemLocation(FLASH,"10 Pokemon Reward",address=0x5d5e8)])
game.key_item_locs.append(game.areas["route_2_gate"].objects[1].itemsHeld[0])
game.newNPC("route_2_gate",2,"Route 2 Catcher")

###Route 2 Trade House###
game.newArea("r2_trade_house","Route 2 Trade House",0x30)
game.newWarp("r2_trade_house",0,"route_2ne",2,"True",[1],[2])
game.newNPC("r2_trade_house",1,"Faint Aide")
game.newNPC("r2_trade_house",2,"Abra -> Mr. Mime Trader")

###Viridian Forest South Gate###
game.newArea("forest_south_gate","Viridian Forest - South Gate",0x32)
game.newWarp("forest_south_gate",0,"viridian_forest",3,"True",[1],[4])
game.newWarp("forest_south_gate",2,"route_2v",5,"True",[3],[5])
game.newNPC("forest_south_gate",1,"Natural Maze Girl")
game.newNPC("forest_south_gate",2,"Rattata Girl")

###Viridian Forest North Gate###
game.newArea("forest_north_gate","Viridian Forest - North Gate",0x2F)
game.newWarp("forest_north_gate",0,"route_2p",1,"True",[1],[1])
game.newWarp("forest_north_gate",2,"viridian_forest",0,"True",[3],[0])
game.newNPC("forest_north_gate",1,"Look Everywhere Dude")
game.newNPC("forest_north_gate",2,"Cut Bushes Guy")

###Viridian Forest###
game.newDungeon("viridian_forest","Viridian Forest",0x33)
game.newWarp("viridian_forest",0,"forest_north_gate",2,"True",[1],[3])
game.newWarp("viridian_forest",2,"forest_south_gate",1,"True",[3,4,5],[1,1,1])
game.newNPC("viridian_forest",1,"Forest Entrance Catcher")
game.newItemLoc("viridian_forest",5,"Antidote",ANTIDOTE,address=0x6122C)
game.newItemLoc("viridian_forest",6,"Potion",POTION,address=0x61233)
game.newItemLoc("viridian_forest",7,"Poke Ball",POKE_BALL,address=0x6123A)
game.newNPC("viridian_forest",8,"Out of Balls Catcher")
game.newHiddenItem("viridian_forest",0,"Hidden Potion",POTION,address=0x46E49)
game.newHiddenItem("viridian_forest",1,"Hidden Antidote",ANTIDOTE,address=0x46E4F)

###Pewter City###
#Main Area
game.newTown("pewter_city","Pewter City",0x02)
game.newExit("pewter_city","route_2p")
game.newExit("pewter_city","route_3","has(BOULDERBADGE)")
game.newExit("pewter_city","pewter_city_back","canCut()")
game.newWarp("pewter_city",0,"museum_1f",0)
game.newWarp("pewter_city",2,"pewter_gym",0)
game.newWarp("pewter_city",3,"pewter_nidoran_house",0)
game.newWarp("pewter_city",4,"pewter_mart",0)
game.newWarp("pewter_city",5,"pewter_speech_house",0)
game.newWarp("pewter_city",6,"pewter_center",0)
game.newNPC("pewter_city",1,"Clefairy Girl")
game.newNPC("pewter_city",2,"Serious Trainer")
game.newNPC("pewter_city",4,"Pewter Gardener")
#Museum Back Entrnce
game.newArea("pewter_city_back","Pewter City - Museum Back",0x02)
game.newWarp("pewter_city_back",1,"museum_back",2)

###Pewter Museum###
#1F
game.newArea("museum_1f","Pewter Museum - 1F",0x34)
game.newWarp("museum_1f",0,"pewter_city",0,"True",[1],[0])
game.newWarp("museum_1f",4,"museum_2f",0)
game.newNPC("museum_1f",2,"Museum Patron")
#2F
game.newArea("museum_2f","Pewter Museum - 2F",0x35)
game.newWarp("museum_2f",0,"museum_1f",4)
game.newNPC("museum_2f",1,"Moon Stone Skeptic")
game.newNPC("museum_2f",2,"Lunar Landing Man")
game.newNPC("museum_2f",3,"Space Exhibit Guide")
game.newNPC("museum_2f",4,"Pikachu Girl")
game.newNPC("museum_2f",5,"Pikachu Girl's Father")
#Back Entrance
game.newArea("museum_back","Pewter Museum - Back",0x34)
game.newWarp("museum_back",2,"pewter_city",1,"True",[3],[1])
game.newNPC("museum_back",3,"Old Amber Scientist",[ItemLocation(OLD_AMBER,"Old Amber",address=0x5c266)])
game.key_item_locs.append(game.areas["museum_back"].objects[3].itemsHeld[0])
game.newNPC("museum_back",4,"Museum Back Scientist")

###Pewter Gym###
game.newArea("pewter_gym","Pewter Gym",0x36)
game.newWarp("pewter_gym",0,"pewter_city",2,"True",[1],[2])
game.newNPC("pewter_gym",1,"Brock",[ItemLocation(BOULDERBADGE,"Brock's Badge"),ItemLocation(TM_34,"Brock's TM",address=0x5C3ED)])
game.npc_item_locs.append(game.areas["viridian_gym"].objects[1].itemsHeld[1])
game.newNPC("pewter_gym",3,"Pewter Gym Guide")

###Pewter Nidoran House###
game.newArea("pewter_nidoran_house","Pewter Nidoran House",0x37)
game.newWarp("pewter_nidoran_house",0,"pewter_city",3,"True",[1],[3])
game.newNPC("pewter_nidoran_house",1,"Nidoran Kid")
game.newNPC("pewter_nidoran_house",2,"Badgeless Man")

###Pewter PokeMart###
game.newArea("pewter_mart","Pewter PokeMart",0x38)
game.newWarp("pewter_mart",0,"pewter_city",4,"True",[1],[4])
game.newNPC("pewter_mart",2,"Swindled Catcher")
game.newNPC("pewter_mart",3,"Diligent Trainer")

###Pewter Speech House###
game.newArea("pewter_speech_house","Pewter Speech House",0x39)
game.newWarp("pewter_speech_house",0,"pewter_city",5,"True",[1],[5])
game.newNPC("pewter_speech_house",1,"Moves Guy")
game.newNPC("pewter_speech_house",2,"Status Effect Tip")

###Pewter Pokemon Center###
game.newArea("pewter_center","Pewter Pokemon Center",0x3A)
game.newWarp("pewter_center",0,"pewter_city",6,"True",[1],[6])
game.newNPC("pewter_center",2,"Gentleman on the Phone")

###Route 3###
game.newArea("route_3","Route 3",0x0E)
game.newExit("route_3","pewter_city","has(BOULDERBADGE)")
game.newExit("route_3","route_4p")
game.newNPC("route_3",1,"Mt. Moon Traveler")

###Route 4###
#Pewter Side
game.newArea("route_4p","Route 4 - Pewter Side",0x0F)
game.newExit("route_4p","route_3")
game.newWarp("route_4p",0,"mt_moon_center",0)
game.newWarp("route_4p",1,"mt_moon_1f",0)
game.newNPC("route_4p",1,"Tripped Over Geodude")
#Cerulean Side
game.newArea("route_4c","Route 4 - Pewter Side",0x0F)
game.newWarp("route_4c",1,"mt_moon_b1f",7)
#game.newExit("route_4c","cerulean_city")
game.newItemLoc("route_4c",3,"TM 04",TM_04,address=0x543DF)
game.newHiddenItem("route_4c",0,"Hidden Great Ball",GREAT_BALL,address=0x470A6)

###Mt. Moon Pokemon Center###
game.newArea("mt_moon_center","Mt. Moon Pokemon Center",0x44)
game.newWarp("mt_moon_center",0,"route_4p",0,"True",[1],[0])
game.newNPC("mt_moon_center",2,"Six Balls Catcher")
game.newNPC("mt_moon_center",3,"Newsreading Gentleman")
game.newNPC("mt_moon_center",4,"Magikarp Salesman")

###Mt. Moon###
#1F
game.newDungeon("mt_moon_1f","Mt. Moon - 1F",0x3B)
game.newWarp("mt_moon_1f",0,"route_4p",1,"True",[1],[1])
game.newWarp("mt_moon_1f",2,"mt_moon_b1f",0,"True",[3,4],[2,3])
game.newItemLoc("mt_moon_1f",8,"Potion",POTION,address=0x49B5F)
game.newItemLoc("mt_moon_1f",9,"Moon Stone",MOON_STONE,address=0x49B66)
game.newItemLoc("mt_moon_1f",10,"Rare Candy",RARE_CANDY,address=0x49B6D)
game.newItemLoc("mt_moon_1f",11,"Escape Rope",ESCAPE_ROPE,address=0x49B74)
game.newItemLoc("mt_moon_1f",12,"Potion 2",POTION,address=0x49B7B)
game.newItemLoc("mt_moon_1f",13,"TM 12",TM_12,address=0x49B82)
#B1F
game.newDungeon("mt_moon_b1f","Mt. Moon - B1F",0x3C)
game.newWarp("mt_moon_b1f",0,"mt_moon_1f",2,"True",[2,3],[3,4])
game.newWarp("mt_moon_b1f",1,"mt_moon_b2f",0,"True",[4,5,6],[1,2,3])
game.newWarp("mt_moon_b1f",7,"route_4c",2)
#B2F
game.newDungeon("mt_moon_b2f","Mt. Moon - B2F",0x3D)
game.newWarp("mt_moon_b2f",0,"mt_moon_b1f",1,"True",[1,2,3],[4,5,6])
game.newKeyItemLoc("mt_moon_b2f",6,"Left Fossil",DOME_FOSSIL,address=0x49ef0)
game.newKeyItemLoc("mt_moon_b2f",7,"Right Fossil",HELIX_FOSSIL,address=0x49f2b)
game.newItemLoc("mt_moon_b2f",8,"HP Up",HP_UP,address=0x4A029)
game.newItemLoc("mt_moon_b2f",9,"TM 01",TM_01,address=0x4A030)

# for n, a in game.areas.items():
#     print(a.name + " - " + str(game.canGetToFromStart(a.id)))

#print(game.canGetToFromStart("museum_back",{CUT,CASCADEBADGE}))
#print(game.canGetToFromStart("museum_back"))
#print(game.canGetToFromStart("route_4c"))
