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
game.newTown("pallet_town","Pallet Town",0x0,0x182C5)
game.newExit("pallet_town","route_1")
#newExit("pallet_town","route_21","canSurf()")
game.newWarp("pallet_town",0,"reds_house_1F",0,"north-red")
game.newWarp("pallet_town",1,"blues_house",0,"north")
game.newWarp("pallet_town",2,"oaks_lab",1,"north-oak")
game.newNPC("pallet_town",2,"Pallet Girl")
game.newNPC("pallet_town",3,"Technology Dude")

###Red's House###
#1F
game.newArea("reds_house_1F","Red's House - 1F",0x25,0x481E6)
game.newWarp("reds_house_1F",0,"pallet_town",0,"south-red","True",[1],[0])
game.newWarp("reds_house_1F",2,"reds_house_2F",0,"stairs-red")
#2F
game.newArea("reds_house_2F","Red's House - 2F",0x26,0x5C0D2)
game.newWarp("reds_house_2F",0,"reds_house_1F",2,"stairs-red")

###Blue's House###
game.newArea('blues_house',"Blue's House",0x27,0x19BD0)
game.newWarp("blues_house",0,"pallet_town",1,"south","True",[1],[1])
game.newNPC("blues_house",1,"Daisy Oak",[ItemLocation(TOWN_MAP,"Map Gift","has(POKEDEX)",address=0x19b7c)])
game.key_item_locs.append(game.areas["blues_house"].objects[1].itemsHeld[0])

###Oak's Lab###
game.newArea("oaks_lab","Prof. Oak's Lab",0x28,0x1D40C)
game.newWarp("oaks_lab",0,"pallet_town",2,"south-oak","True",[1],[2])
game.newNPC("oaks_lab",0,"Prof. Oak",[ItemLocation(POKEDEX, "Parcel Exchange","has(OAKS_PARCEL)")])
#Oak will never be randomized (it would just break things too much otherwise), so it's okay
#if he's object number 0
game.newNPC("oaks_lab",7,"Lab Girl")
game.newNPC("oaks_lab",8,"Lab Aide 1")
game.newNPC("oaks_lab",9,"Lab Aide 2")

###Route 1###
game.newArea("route_1","Route 1",0x0C,0)
game.newExit("route_1","pallet_town")
game.newExit("route_1","viridian_city")
game.newNPC("route_1",1,"Potion Guy",[ItemLocation(POTION,"Free Potion",address=0x1CACA)])
game.npc_item_locs.append(game.areas["route_1"].objects[1].itemsHeld[0])
game.newNPC("route_1",2,"Ledge Dude")

###Viridian City###
#Main Area
game.newTown("viridian_city","Viridian City",0x01,0x18386)
game.newExit("viridian_city","route_1")
#newExit("viridian_city","route_22")
game.newExit("viridian_city","viridian_north","has(POKEDEX) or canCut()")
game.newWarp("viridian_city",0,"viridian_center",0,"north")
game.newWarp("viridian_city",1,"viridian_mart",0,"north")
game.newWarp("viridian_city",2,"viridian_school",0,"north")
game.newWarp("viridian_city",3,"viridian_house",0,"north")
game.newNPC("viridian_city",1,"Pokeball Kid")
game.newNPC("viridian_city",3,"Caterpillar Kid")
game.newNPC("viridian_city",6,"Dream Eater Guy",[ItemLocation(TM_42,"Dream Eater TM",address=0x191A6)],"canCut() or canSurf()")
game.npc_item_locs.append(game.areas["viridian_city"].objects[6].itemsHeld[0])
game.newNPC("viridian_city",7,"Old Man",req="has(POKEDEX)")
game.newHiddenItem("viridian_city",0,"Hidden Potion on Tree",POTION,address=0x46F8F)
#Above old man
game.newArea("viridian_north","Viridian City - North Part",0x01,0x18386)
game.newExit("viridian_north","viridian_city","has(POKEDEX) or canCut()")
game.newExit("viridian_north","route_2v")
game.newNPC("viridian_north",2,"Viridian Gym Bystander")
game.newWarp("viridian_north",4,"viridian_gym",0,"north","firstSevenBadges()")

###Viridian Pokemon Center###
game.newArea("viridian_center","Viridian Pokemon Center",0x29,0x44279)
game.newWarp("viridian_center",0,"viridian_city",0,"south","True",[1],[0])
game.newNPC("viridian_center",2,"PC Gentleman")
game.newNPC("viridian_center",3,"Free Healthcare Kid")

###Viridian PokeMart###
game.newArea("viridian_mart","Viridian PokeMart",0x2A,0x1D50C)
game.newWarp("viridian_mart",0,"viridian_city",1,"south","True",[1],[1])
game.newNPC("viridian_mart",0,"Viridian Shopkeeper",[ItemLocation(OAKS_PARCEL,"Parcel Pickup")])
game.newNPC("viridian_mart",2,"Antidote Shopper")
game.newNPC("viridian_mart",3,"Sold-Out Potion Shopper")

###Viridian Schoolhouse###
game.newArea("viridian_school","Viridian Schoolhouse",0x2B,0x1D55F)
game.newWarp("viridian_school",0,"viridian_city",2,"south","True",[1],[2])
game.newNPC("viridian_school",1,"Viridian Student")
game.newNPC("viridian_school",2,"Viridian Teacher")

###Viridian Nickname House###
game.newArea("viridian_house","Viridian Nickname House",0x2C,0x1D5BD)
game.newWarp("viridian_house",0,"viridian_city",3,"south","True",[1],[3])
game.newNPC("viridian_house",1,"Viridian Father")
game.newNPC("viridian_house",2,"Viridian Daughter")

###Viridian Gym###
game.newArea("viridian_gym","Viridian Gym",0x2D,0x74BE0)
game.newWarp("viridian_gym",0,"viridian_north",4,"south","True",[1],[4])
game.newNPC("viridian_gym",1,"Giovanni",[ItemLocation(EARTHBADGE,"Giovanni's Badge"),ItemLocation(TM_27,"Giovanni's TM",address=0x749A3)])
game.npc_item_locs.append(game.areas["viridian_gym"].objects[1].itemsHeld[1])
game.newNPC("viridian_gym",10,"Viridian Gym Guide")
game.newItemLoc("viridian_gym",11,"Revive",REVIVE,address=0x74C3E)

###Route 2###
#Viridian Side (south)
game.newArea("route_2v","Route 2 - Viridian Side",0x0D,0x54024)
game.newExit("route_2v","viridian_city","has(POKEDEX)")
game.newWarp("route_2v",5,"forest_south_gate",2,"north")
game.newExit("route_2v","route_2se","canCut()")
#Southeast Section
game.newArea("route_2se","Route 2 - Southeast Section",0x0D,0x54024)
game.newExit("route_2se","route_2v","canCut()")
game.newWarp("route_2se",4,"route_2_gate",2,"north")
game.newItemLoc("route_2se",1,"Moon Stone",MOON_STONE,address=0x5404A)
game.newItemLoc("route_2se",2,"HP Up",HP_UP,address=0x54051)
#Mideast Section
game.newArea("route_2m","Route 2 - Mideast Section",0x0D,0x54024)
game.newExit("route_2m","route_2ne","canCut()")
game.newWarp("route_2m",3,"route_2_gate",1,"south")
#Northeast Section
game.newArea("route_2ne","Route 2 - Northeast Section",0x0D,0x54024)
game.newExit("route_2ne","route_2m","canCut()")
game.newExit("route_2ne","route_2p","canCut()")
#game.newWarp("route_2ne",0,"diglett_cave_r2",0,"north")
game.newWarp("route_2ne",2,"r2_trade_house",0,"north")
#Pewter Side (north)
game.newArea("route_2p","Route 2 - Pewter Side",0x0D,0x54024)
game.newExit("route_2p","pewter_city")
game.newExit("route_2p","route_2ne","canCut()")
game.newWarp("route_2p",1,"forest_north_gate",1,"south")

###Route 2 Gate###
game.newArea("route_2_gate","Route 2 Gate",0x31,0x5D622)
game.newWarp("route_2_gate",0,"route_2m",3,"north","True",[1],[3])
game.newWarp("route_2_gate",2,"route_2se",4,"south","True",[3],[4])
game.newNPC("route_2_gate",1,"Flash Aide",[ItemLocation(FLASH,"10 Pokemon Reward",address=0x5d5e8)])
game.key_item_locs.append(game.areas["route_2_gate"].objects[1].itemsHeld[0])
game.newNPC("route_2_gate",2,"Route 2 Catcher")

###Route 2 Trade House###
game.newArea("r2_trade_house","Route 2 Trade House",0x30,0x1DF09)
game.newWarp("r2_trade_house",0,"route_2ne",2,"south","True",[1],[2])
game.newNPC("r2_trade_house",1,"Faint Aide")
game.newNPC("r2_trade_house",2,"Abra -> Mr. Mime Trader")

###Viridian Forest South Gate###
game.newArea("forest_south_gate","Viridian Forest - South Gate",0x32,0x5D66F)
game.newWarp("forest_south_gate",0,"viridian_forest",3,"north","True",[1],[4])
game.newWarp("forest_south_gate",2,"route_2v",5,"south","True",[3],[5])
game.newNPC("forest_south_gate",1,"Natural Maze Girl")
game.newNPC("forest_south_gate",2,"Rattata Girl")

###Viridian Forest North Gate###
game.newArea("forest_north_gate","Viridian Forest - North Gate",0x2F,0x5D59A)
game.newWarp("forest_north_gate",0,"route_2p",1,"north","True",[1],[1])
game.newWarp("forest_north_gate",2,"viridian_forest",0,"south","True",[3],[0])
game.newNPC("forest_north_gate",1,"Look Everywhere Dude")
game.newNPC("forest_north_gate",2,"Cut Bushes Guy")

###Viridian Forest###
game.newDungeon("viridian_forest","Viridian Forest",0x33,0x611DC)
game.newWarp("viridian_forest",0,"forest_north_gate",2,"north","True",[1],[3])
game.newWarp("viridian_forest",2,"forest_south_gate",1,"south","True",[3,4,5],[1,1,1])
game.newNPC("viridian_forest",1,"Forest Entrance Catcher")
game.newItemLoc("viridian_forest",5,"Antidote",ANTIDOTE,address=0x6122C)
game.newItemLoc("viridian_forest",6,"Potion",POTION,address=0x61233)
game.newItemLoc("viridian_forest",7,"Poke Ball",POKE_BALL,address=0x6123A)
game.newNPC("viridian_forest",8,"Out of Balls Catcher")
game.newHiddenItem("viridian_forest",0,"Hidden Potion",POTION,address=0x46E49)
game.newHiddenItem("viridian_forest",1,"Hidden Antidote",ANTIDOTE,address=0x46E4F)

###Pewter City###
#Main Area
game.newTown("pewter_city","Pewter City",0x02,0x18579)
game.newExit("pewter_city","route_2p")
game.newExit("pewter_city","route_3","has(BOULDERBADGE)")
game.newExit("pewter_city","pewter_city_back","canCut()")
game.newWarp("pewter_city",0,"museum_1f",0,"north")
game.newWarp("pewter_city",2,"pewter_gym",0,"north")
game.newWarp("pewter_city",3,"pewter_nidoran_house",0,"north")
game.newWarp("pewter_city",4,"pewter_mart",0,"north")
game.newWarp("pewter_city",5,"pewter_speech_house",0,"north")
game.newWarp("pewter_city",6,"pewter_center",0,"north")
game.newNPC("pewter_city",1,"Clefairy Girl")
game.newNPC("pewter_city",2,"Serious Trainer")
game.newNPC("pewter_city",4,"Pewter Gardener")
#Museum Back Entrnce
game.newArea("pewter_city_back","Pewter City - Museum Back",0x02,0x18579)
game.newWarp("pewter_city_back",1,"museum_back",2,"north")

###Pewter Museum###
#1F
game.newArea("museum_1f","Pewter Museum - 1F",0x34,0x5C2C3)
game.newWarp("museum_1f",0,"pewter_city",0,"south","True",[1],[0])
game.newWarp("museum_1f",4,"museum_2f",0,"stairs")
game.newNPC("museum_1f",2,"Museum Patron")
#2F
game.newArea("museum_2f","Pewter Museum - 2F",0x35,0x5C34D)
game.newWarp("museum_2f",0,"museum_1f",4,"stairs")
game.newNPC("museum_2f",1,"Moon Stone Skeptic")
game.newNPC("museum_2f",2,"Lunar Landing Man")
game.newNPC("museum_2f",3,"Space Exhibit Guide")
game.newNPC("museum_2f",4,"Pikachu Girl")
game.newNPC("museum_2f",5,"Pikachu Girl's Father")
#Back Entrance
game.newArea("museum_back","Pewter Museum - Back",0x34,0x5C2C3)
game.newWarp("museum_back",2,"pewter_city",1,"south","True",[3],[1])
game.newNPC("museum_back",3,"Old Amber Scientist",[ItemLocation(OLD_AMBER,"Old Amber",address=0x5c266)])
game.key_item_locs.append(game.areas["museum_back"].objects[3].itemsHeld[0])
game.newNPC("museum_back",4,"Museum Back Scientist")

###Pewter Gym###
game.newArea("pewter_gym","Pewter Gym",0x36,0x5c530)
game.newWarp("pewter_gym",0,"pewter_city",2,"south","True",[1],[2])
game.newNPC("pewter_gym",1,"Brock",[ItemLocation(BOULDERBADGE,"Brock's Badge"),ItemLocation(TM_34,"Brock's TM",address=0x5C3ED)])
game.npc_item_locs.append(game.areas["viridian_gym"].objects[1].itemsHeld[1])
game.newNPC("pewter_gym",3,"Pewter Gym Guide")

###Pewter Nidoran House###
game.newArea("pewter_nidoran_house","Pewter Nidoran House",0x37,0x1d618)
game.newWarp("pewter_nidoran_house",0,"pewter_city",3,"south","True",[1],[3])
game.newNPC("pewter_nidoran_house",1,"Nidoran Kid")
game.newNPC("pewter_nidoran_house",2,"Badgeless Man")

###Pewter PokeMart###
game.newArea("pewter_mart","Pewter PokeMart",0x38,0x74cdc)
game.newWarp("pewter_mart",0,"pewter_city",4,"south","True",[1],[4])
game.newNPC("pewter_mart",2,"Swindled Catcher")
game.newNPC("pewter_mart",3,"Diligent Trainer")

###Pewter Speech House###
game.newArea("pewter_speech_house","Pewter Speech House",0x39,0x1D65B)
game.newWarp("pewter_speech_house",0,"pewter_city",5,"south","True",[1],[5])
game.newNPC("pewter_speech_house",1,"Moves Guy")
game.newNPC("pewter_speech_house",2,"Status Effect Tip")

###Pewter Pokemon Center###
game.newArea("pewter_center","Pewter Pokemon Center",0x3A,0x5C60F)
game.newWarp("pewter_center",0,"pewter_city",6,"south","True",[1],[6])
game.newNPC("pewter_center",2,"Gentleman on the Phone")

###Route 3###
game.newArea("route_3","Route 3",0x0E,0)
game.newExit("route_3","pewter_city","has(BOULDERBADGE)")
game.newExit("route_3","route_4p")
game.newNPC("route_3",1,"Mt. Moon Traveler")

###Route 4###
#Pewter Side
game.newArea("route_4p","Route 4 - Pewter Side",0x0F,0x543B4)
game.newExit("route_4p","route_3")
game.newWarp("route_4p",0,"mt_moon_center",0,"north")
game.newWarp("route_4p",1,"mt_moon_1f",0,"north")
game.newNPC("route_4p",1,"Tripped Over Geodude")
#Cerulean Side
game.newArea("route_4c","Route 4 - Pewter Side",0x0F,0x543B4)
game.newWarp("route_4c",1,"mt_moon_b1f_exit",7,"north")
#game.newExit("route_4c","cerulean_city")
game.newItemLoc("route_4c",3,"TM 04",TM_04,address=0x543DF)
game.newHiddenItem("route_4c",0,"Hidden Great Ball",GREAT_BALL,address=0x470A6)

###Mt. Moon Pokemon Center###
game.newArea("mt_moon_center","Mt. Moon Pokemon Center",0x44,0x49378)
game.newWarp("mt_moon_center",0,"route_4p",0,"south","True",[1],[0])
game.newNPC("mt_moon_center",2,"Six Balls Catcher")
game.newNPC("mt_moon_center",3,"Newsreading Gentleman")
game.newNPC("mt_moon_center",4,"Magikarp Salesman")

###Mt. Moon###
#1F
game.newDungeon("mt_moon_1f","Mt. Moon - 1F",0x3B,0x49B08)
game.newWarp("mt_moon_1f",0,"route_4p",1,"south","True",[1],[1])
game.newWarp("mt_moon_1f",2,"mt_moon_b1f_l",0,"stairs")
game.newWarp("mt_moon_1f",4,"mt_moon_b1f_backl",3,"stairs")
game.newWarp("mt_moon_1f",3,"mt_moon_b1f_short",2,"stairs")
game.newItemLoc("mt_moon_1f",8,"Potion",POTION,address=0x49B5F)
game.newItemLoc("mt_moon_1f",9,"Moon Stone",MOON_STONE,address=0x49B66)
game.newItemLoc("mt_moon_1f",10,"Rare Candy",RARE_CANDY,address=0x49B6D)
game.newItemLoc("mt_moon_1f",11,"Escape Rope",ESCAPE_ROPE,address=0x49B74)
game.newItemLoc("mt_moon_1f",12,"Potion 2",POTION,address=0x49B7B)
game.newItemLoc("mt_moon_1f",13,"TM 12",TM_12,address=0x49B82)
#B1F - L-Shaped Corridor
game.newDungeon("mt_moon_b1f_l","Mt. Moon - B1F - L-Shaped Corridor",0x3C,0x51A4f)
game.newWarp("mt_moon_b1f_l",0,"mt_moon_1f",2,"stairs")
game.newWarp("mt_moon_b1f_l",4,"mt_moon_b2f_outside",1,"stairs")
#B1F - Backwards-L Corridor
game.newDungeon("mt_moon_b1f_backl","Mt. Moon - B1F - Backwards-L Corridor",0x3C,0x51A4f)
game.newWarp("mt_moon_b1f_backl",3,"mt_moon_1f",4,"stairs")
game.newWarp("mt_moon_b1f_backl",5,"mt_moon_b2f_south",2,"stairs")
#B1F - Short Center Corridor
game.newDungeon("mt_moon_b1f_short","Mt. Moon - B1F - Short Center Corridor",0x3C,0x51A4f)
game.newWarp("mt_moon_b1f_short",2,"mt_moon_1f",3,"stairs")
game.newWarp("mt_moon_b1f_short",1,"mt_moon_b2f_north",0,"stairs")
#B1F - Exit
game.newDungeon("mt_moon_b1f_exit","Mt. Moon - B1F - Exit",0x3C,0x51A4f)
game.newWarp("mt_moon_b1f_exit",6,"mt_moon_b2f_outside",3,"stairs")
game.newWarp("mt_moon_b1f_exit",7,"route_4c",2,"stairs")
#B2F - South Section
game.newDungeon("mt_moon_b2f_south","Mt. Moon - B2F - South Section",0x3D,0x49FDD)
game.newWarp("mt_moon_b2f_south",2,"mt_moon_b1f_backl",5,"stairs")
game.newItemLoc("mt_moon_b2f_south",8,"HP Up",HP_UP,address=0x4A029)
#B2F - North Section
game.newDungeon("mt_moon_b2f_north","Mt. Moon - B2F - South Section",0x3D,0x49FDD)
game.newWarp("mt_moon_b2f_north",0,"mt_moon_b1f_short",1,"stairs")
game.newItemLoc("mt_moon_b2f_north",9,"TM 01",TM_01,address=0x4A030)
game.newHiddenItem("mt_moon_b2f_north",1,"Hidden Ether",ETHER,address=0x46E5C)
#B2F - Outside Section
game.newDungeon("mt_moon_b2f_outside","Mt. Moon - B2F - Outside Section",0x3D,0x49FDD)
game.newWarp("mt_moon_b2f_outside",1,"mt_moon_b1f_l",4,"stairs")
game.newWarp("mt_moon_b2f_outside",3,"mt_moon_b1f_exit",6,"stairs")
game.newKeyItemLoc("mt_moon_b2f_outside",6,"Left Fossil",DOME_FOSSIL,address=0x49ef0)
game.newKeyItemLoc("mt_moon_b2f_outside",7,"Right Fossil",HELIX_FOSSIL,address=0x49f2b)
game.newHiddenItem("mt_moon_b2f_outside",0,"Hidden Moon Stone",MOON_STONE,address=0x46E56)



# for n, a in game.areas.items():
#     print(a.name + " - " + str(game.canGetToFromStart(a.id)))

#print(game.canGetToFromStart("museum_back",{CUT,CASCADEBADGE}))
#print(game.canGetToFromStart("museum_back"))
#print(game.canGetToFromStart("route_4c"))
