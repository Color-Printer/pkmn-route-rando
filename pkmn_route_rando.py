class Area:
    def __init__(self,name,identifier,mapid):
        self.name = name
        self.id = identifier
        self.mapid = mapid
        self.exits = []
        self.objects = {}
        self.hiddenItems = {}

    def __str__(self):
        s = "---" + self.name + "---"
        for e in self.exits:
            s = s + "\n" + str(e)
        for n, i in self.objects.items():
            s = s + "\nObject " + str(n) + ": " + str(i)
        for n2, h in self.hiddenItems.items():
            s = s + "\n" + str(h)
        return s

    def canUseExit(self,exitNum):
        return self.exits[exitNum].canUse()

    def getAllItems(self,items):
        for n, i in self.objects.items():
            if isinstance(i,ItemLocation):
                i.get(items)
            elif isinstance(i,NPC):
                i.getItems(items)
        for n2, h in self.hiddenItems.items():
            h.get(items)

    def getWarp(self,w_id):
        for x in self.exits:
            if isinstance(x,Warp):
                if x.warp_id == w_id:
                    return x
        return False

    def directAccess(self,area): # can reach area with no items
        for x in self.exits:
            if x.destination == area and x.requirements == "True":
                    return True
        return False

    def getAllValidExits(self):
        v = []
        for x in self.exits:
            if x.canUse() and x.destination not in v:
                v.append(x.destination)
        return v

    def getAllGraphConnections(self):
        c = set()
        for x in self.exits:
            c.add(x.destination)
        return c

class Town(Area):
    pass

class Dungeon(Area):
    pass

class Exit:
    def __init__(self,dest_id,req="True"):
        self.destination = dest_id
        self.requirements = req

    def __str__(self):
        s = "Exit to " + areas[self.destination].name
        if self.requirements != "True":
            s = s + "\n- Requirements: " + self.requirements
        return s

    def canUse(self):
        return eval(self.requirements)

    def otherEnd(self):
        return areas[self.destination]

    def otherEndID(self):
        return areas[self.destination].mapid

class Warp(Exit):
    def __init__(self,warp_id,dest_id,dest_warp_id,req="True",extra=[],extra_dest=[]):
        super().__init__(dest_id,req)
        self.warp_id = warp_id
        self.extra_warp_id = extra
        self.dest_warp_id = dest_warp_id
        self.extra_dest_warp_id = extra_dest

    def __str__(self):
        s= "Warp (ID: " + str(self.warp_id) + ") to " + areas[self.destination].name + \
               " (warp-to ID: " + str(self.dest_warp_id) + ")"
        if self.requirements != "True":
            s = s + "\n- Requirements: " + self.requirements
        return s

class ItemLocation:
    def __init__(self,item,name,req="True"):
        self.item = item
        self.requirements = req
        self.name = name

    def __str__(self):
        s = self.name + ": " + self.item
        if self.requirements != "True":
            s = s + " - Requirements: " + self.requirements
        return s

    def canAccess(self):
        return eval(self.requirements)

    def get(self,items):
        if self.canAccess():
            items.add(self.item)

class HiddenItem(ItemLocation):
    def canAccess(self):
        return eval(self.requirements + " and has('itemfinder')")

class NPC:
    def __init__(self,name,items=[],req="True"):
        self.name = name
        self.itemsHeld = items
        self.requirements = req

    def __str__(self):
        s="NPC (" + self.name + ")"
        for i in self.itemsHeld:
            s = s + "\n- " + str(i)
        if self.requirements != "True":
            s = s + "\n- Requirements: " + self.requirements
        return s

    def canAccess(self):
        return eval(self.requirements)

    def getItems(self,items):
        if self.canAccess():
            for i in self.itemsHeld:
                i.get(items)

areas = {}
inventory = set()

def has(item):
    return item in inventory

def canCut():
    return has("cut") and has("cascadebadge")

def canSurf():
    return has("surf") and has("soulbadge")

def canStrength():
    return has("strength") and has("rainbowbadge")

def canFlash():
    return has("flash") and has("boulderbadge")

def firstSevenBadges():
    return has("boulderbadge") and has("cascadebadge") and has("thunderbadge") and \
           has("rainbowbadge") and has("soulbadge") and has("marshbadge") and \
           has("volcanobadge")

def allBadges():
    return sevenBadges() and has("earthbadge")

def newArea(id,name,map_id):
    areas[id] = Area(name,id,map_id)

def newTown(id,name,map_id):
    areas[id] = Town(name,id,map_id)

def newDungeon(id,name,map_id):
    areas[id] = Dungeon(name,id,map_id)

def newExit(id,dest_id,req="True"):
    areas[id].exits.append(Exit(dest_id,req))

def newWarp(id,w_id,dest_id,dest_w_id,req="True",extra=[],extra_dest=[]):
    areas[id].exits.append(Warp(w_id,dest_id,dest_w_id,req,extra,extra_dest))

def newItemLoc(id,o_id,name,item,req="True"):
    areas[id].objects[o_id] = ItemLocation(item,name,req)

def newNPC(id,o_id,name,items=[],req="True"):
    areas[id].objects[o_id] = NPC(name,items,req)

def newHiddenItem(id,o_id,name,item,req="True"):
    areas[id].hiddenItems[o_id] = ItemLocation(item,name,req)

def clearReachableFlags():
    for n, a in areas.items():
        a.reachable = False

def clearVisitedFlags():
    for n, a in areas.items():
        a.visited = False

def clearBridgeFlags():
    clearVisitedFlags()
    for n, a in areas.items():
        a.disc = float("Inf")
        a.low = float("Inf")
        a.parent = None

def canGetFromTo(start,goal,i=set()):
    clearReachableFlags()
    inventory.clear()
    inventory.update(i)
    newPlaces = True
    areas[start].reachable = True
    while newPlaces == True:
        clearVisitedFlags()
        Q = []
        areas[start].visited = True
        Q.append(start)
        while len(Q) > 0:
            v = Q.pop()
            if v == goal:
                return True
            e = areas[v].getAllValidExits()
            for w in e:
                if areas[w].visited == False:
                    areas[w].visited = True
                    Q.append(w)
        newPlaces = False
        numItems = len(inventory)
        for n, a in areas.items():
            if a.visited == True:
                if a.reachable == False:
                    newPlaces = True
                    a.reachable = True
                a.getAllItems(inventory)
        if len(inventory) > numItems:
            newPlaces = True
    return areas[goal].reachable

def canGetToFromStart(goal,i=set()):
    return canGetFromTo("reds_house_2F",goal,i)

bridge_time = 0

def bridgeHelper(node):
    global bridge_time
    node.visited = True
    node.disc = bridge_time
    node.low = bridge_time
    bridge_time += 1

    edges = node.getAllGraphConnections()
    for e in edges:
        other_end = areas[e]
        if other_end.visited == False:
            other_end.parent = node
            bridgeHelper(other_end)
            node.low = min(node.low,other_end.low)
            if other_end.low > node.disc:
                print(node.name + " - " + other_end.name)
        elif other_end != node.parent:
            node.low = min(node.low,other_end.disc)

def findBridges():
    clearBridgeFlags()
    bridge_time = 0
    for n, a in areas.items():
        if a.visited == False:
            bridgeHelper(a)

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
newTown("pallet_town","Pallet Town",0x0)
newExit("pallet_town","route_1")
#newExit("pallet_town","route_21","canSurf()")
newWarp("pallet_town",0,"reds_house_1F",0)
newWarp("pallet_town",1,"blues_house",0)
newWarp("pallet_town",2,"oaks_lab",1)
newNPC("pallet_town",2,"Pallet Girl")
newNPC("pallet_town",3,"Technology Dude")

###Red's House###
#1F
newArea("reds_house_1F","Red's House - 1F",0x25)
newWarp("reds_house_1F",0,"pallet_town",0,"True",[1],[0])
newWarp("reds_house_1F",2,"reds_house_2F",0)
#2F
newArea("reds_house_2F","Red's House - 2F",0x26)
newWarp("reds_house_2F",0,"reds_house_1F",2)

###Blue's House###
newArea('blues_house',"Blue's House",0x27)
newWarp("blues_house",0,"pallet_town",1,"True",[1],[1])
newNPC("blues_house",1,"Daisy Oak",[ItemLocation("town map","Map Gift","has('pokedex')")])

###Oak's Lab###
newArea("oaks_lab","Prof. Oak's Lab",0x28)
newWarp("oaks_lab",0,"pallet_town",2,"True",[1],[2])
newNPC("oaks_lab",0,"Prof. Oak",[ItemLocation("pokedex", "Parcel Exchange","has('oak parcel')")])
#Oak will never be randomized (it would just break things too much otherwise), so it's okay
#if he's object number 0
newNPC("oaks_lab",7,"Lab Girl")
newNPC("oaks_lab",8,"Lab Aide 1")
newNPC("oaks_lab",9,"Lab Aide 2")

###Route 1###
newArea("route_1","Route 1",0x0C)
newExit("route_1","pallet_town")
newExit("route_1","viridian_city")
newNPC("route_1",1,"Potion Guy",[ItemLocation("potion","Free Potion")])
newNPC("route_1",2,"Ledge Dude")

###Viridian City###
newTown("viridian_city","Viridian City",0x01)
newExit("viridian_city","route_1")
#newExit("viridian_city","route_22")
newExit("viridian_city","route_2v","has('pokedex')")
newWarp("viridian_city",0,"viridian_center",0)
newWarp("viridian_city",1,"viridian_mart",0)
newWarp("viridian_city",2,"viridian_school",0)
newWarp("viridian_city",3,"viridian_house",0)
newWarp("viridian_city",4,"viridian_gym",0,"firstSevenBadges()")
newNPC("viridian_city",1,"Pokeball Kid")
newNPC("viridian_city",2,"Viridian Gym Bystander")
newNPC("viridian_city",3,"Caterpillar Kid")
newNPC("viridian_city",6,"Dream Eater Guy",[ItemLocation("TM42","Dream Eater TM")],"canCut() or canSurf()")
newNPC("viridian_city",7,"Old Man",req="has('pokedex')")
newHiddenItem("viridian_city",0,"Hidden Potion on Tree","potion")

###Viridian Pokemon Center###
newArea("viridian_center","Viridian Pokemon Center",0x29)
newWarp("viridian_center",0,"viridian_city",0,"True",[1],[0])
newNPC("viridian_center",2,"PC Gentleman")
newNPC("viridian_center",3,"Free Healthcare Kid")

###Viridian PokeMart###
newArea("viridian_mart","Viridian PokeMart",0x2A)
newWarp("viridian_mart",0,"viridian_city",1,"True",[1],[1])
newNPC("viridian_mart",0,"Viridian Shopkeeper",[ItemLocation("oak parcel","Parcel Pickup")])
newNPC("viridian_mart",2,"Antidote Shopper")
newNPC("viridian_mart",3,"Sold-Out Potion Shopper")

###Viridian Schoolhouse###
newArea("viridian_school","Viridian Schoolhouse",0x2B)
newWarp("viridian_school",0,"viridian_city",2,"True",[1],[2])
newNPC("viridian_school",1,"Viridian Student")
newNPC("viridian_school",2,"Viridian Teacher")

###Viridian Nickname House###
newArea("viridian_house","Viridian Nickname House",0x2C)
newWarp("viridian_house",0,"viridian_city",3,"True",[1],[3])
newNPC("viridian_house",1,"Viridian Father")
newNPC("viridian_house",2,"Viridian Daughter")

###Viridian Gym###
newArea("viridian_gym","Viridian Gym",0x2D)
newWarp("viridian_gym",0,"viridian_city",4,"True",[1],[4])
newNPC("viridian_gym",1,"Giovanni",[ItemLocation("earthbadge","Giovanni's Badge"),ItemLocation("TM27","Giovanni's TM")])
newNPC("viridian_gym",10,"Viridian Gym Guide")
newItemLoc("viridian_gym",11,"Revive","revive")

###Route 2###
#Viridian Side (south)
newArea("route_2v","Route 2 - Viridian Side",0x0D)
newExit("route_2v","viridian_city","has('pokedex')")
newWarp("route_2v",5,"forest_south_gate",2)
newExit("route_2v","route_2se","canCut()")
#Southeast Section
newArea("route_2se","Route 2 - Southeast Section",0x0D)
newExit("route_2se","route_2v","canCut()")
newWarp("route_2se",4,"route_2_gate",2)
newItemLoc("route_2se",1,"Moon Stone","moon stone")
newItemLoc("route_2se",2,"HP Up","hp up")
#Mideast Section
newArea("route_2m","Route 2 - Mideast Section",0x0D)
newExit("route_2m","route_2ne","canCut()")
newWarp("route_2m",3,"route_2_gate",1)
#Northeast Section
newArea("route_2ne","Route 2 - Northeast Section",0x0D)
newExit("route_2ne","route_2m","canCut()")
newExit("route_2ne","route_2p","canCut()")
#newWarp("route_2ne",0,"diglett_cave_r2",0)
newWarp("route_2ne",2,"r2_trade_house",0)
#Pewter Side (north)
newArea("route_2p","Route 2 - Pewter Side",0x0D)
newExit("route_2p","pewter_city")
newExit("route_2p","route_2ne","canCut()")
newWarp("route_2p",1,"forest_north_gate",1)

###Route 2 Gate###
newArea("route_2_gate","Route 2 Gate",0x31)
newWarp("route_2_gate",0,"route_2m",3,"True",[1],[3])
newWarp("route_2_gate",2,"route_2se",4,"True",[3],[4])
newNPC("route_2_gate",1,"Flash Aide",[ItemLocation("flash","10 Pokemon Reward")])
newNPC("route_2_gate",2,"Route 2 Catcher")

###Route 2 Trade House###
newArea("r2_trade_house","Route 2 Trade House",0x30)
newWarp("r2_trade_house",0,"route_2ne",2,"True",[1],[2])
newNPC("r2_trade_house",1,"Faint Aide")
newNPC("r2_trade_house",2,"Abra -> Mr. Mime Trader")

###Viridian Forest South Gate###
newArea("forest_south_gate","Viridian Forest - South Gate",0x32)
newWarp("forest_south_gate",0,"viridian_forest",3,"True",[1],[4])
newWarp("forest_south_gate",2,"route_2v",5,"True",[3],[5])
newNPC("forest_south_gate",1,"Natural Maze Girl")
newNPC("forest_south_gate",2,"Rattata Girl")

###Viridian Forest North Gate###
newArea("forest_north_gate","Viridian Forest - North Gate",0x2F)
newWarp("forest_north_gate",0,"route_2p",1,"True",[1],[1])
newWarp("forest_north_gate",2,"viridian_forest",0,"True",[3],[0])
newNPC("forest_north_gate",1,"Look Everywhere Dude")
newNPC("forest_north_gate",2,"Cut Bushes Guy")

###Viridian Forest###
newDungeon("viridian_forest","Viridian Forest",0x33)
newWarp("viridian_forest",0,"forest_north_gate",2,"True",[1],[3])
newWarp("viridian_forest",2,"forest_south_gate",1,"True",[3,4,5],[1,1,1])
newNPC("viridian_forest",1,"Forest Entrance Catcher")
newItemLoc("viridian_forest",5,"Antidote","antidote")
newItemLoc("viridian_forest",6,"Potion","potion")
newItemLoc("viridian_forest",7,"Poke Ball","poke ball")
newNPC("viridian_forest",8,"Out of Balls Catcher")
newHiddenItem("viridian_forest",0,"Hidden Potion","potion")
newHiddenItem("viridian_forest",1,"Hidden Antidote","antidote")

###Pewter City###
#Main Area
newTown("pewter_city","Pewter City",0x02)
newExit("pewter_city","route_2p")
newExit("pewter_city","route_3","has('boulderbadge')")
newExit("pewter_city","pewter_city_back","canCut()")
newWarp("pewter_city",0,"museum_1f",0)
newWarp("pewter_city",2,"pewter_gym",0)
newWarp("pewter_city",3,"pewter_nidoran_house",0)
newWarp("pewter_city",4,"pewter_mart",0)
newWarp("pewter_city",5,"pewter_speech_house",0)
newWarp("pewter_city",6,"pewter_center",0)
newNPC("pewter_city",1,"Clefairy Girl")
newNPC("pewter_city",2,"Serious Trainer")
newNPC("pewter_city",4,"Pewter Gardener")
#Museum Back Entrnce
newArea("pewter_city_back","Pewter City - Museum Back",0x02)
newWarp("pewter_city_back",1,"museum_back",2)

###Pewter Museum###
#1F
newArea("museum_1f","Pewter Museum - 1F",0x34)
newWarp("museum_1f",0,"pewter_city",0,"True",[1],[0])
newWarp("museum_1f",4,"museum_2f",0)
newNPC("museum_1f",2,"Museum Patron")
#2F
newArea("museum_2f","Pewter Museum - 2F",0x35)
newWarp("museum_2f",0,"museum_1f",4)
newNPC("museum_2f",1,"Moon Stone Skeptic")
newNPC("museum_2f",2,"Lunar Landing Man")
newNPC("museum_2f",3,"Space Exhibit Guide")
newNPC("museum_2f",4,"Pikachu Girl")
newNPC("museum_2f",5,"Pikachu Girl's Father")
#Back Entrance
newArea("museum_back","Pewter Museum - Back",0x34)
newWarp("museum_back",2,"pewter_city",1,"True",[3],[1])
newNPC("museum_back",3,"Old Amber Scientist",[ItemLocation("old amber","Old Amber")])
newNPC("museum_back",4,"Museum Back Scientist")

###Pewter Gym###
newArea("pewter_gym","Pewter Gym",0x36)
newWarp("pewter_gym",0,"pewter_city",2,"True",[1],[2])
newNPC("pewter_gym",1,"Brock",[ItemLocation("boulderbadge","Brock's Badge"),ItemLocation("TM34","Brock's TM")])
newNPC("pewter_gym",3,"Pewter Gym Guide")

###Pewter Nidoran House###
newArea("pewter_nidoran_house","Pewter Nidoran House",0x37)
newWarp("pewter_nidoran_house",0,"pewter_city",3,"True",[1],[3])
newNPC("pewter_nidoran_house",1,"Nidoran Kid")
newNPC("pewter_nidoran_house",2,"Badgeless Man")

###Pewter PokeMart###
newArea("pewter_mart","Pewter PokeMart",0x38)
newWarp("pewter_mart",0,"pewter_city",4,"True",[1],[4])
newNPC("pewter_mart",2,"Swindled Catcher")
newNPC("pewter_mart",3,"Diligent Trainer")

###Pewter Speech House###
newArea("pewter_speech_house","Pewter Speech House",0x39)
newWarp("pewter_speech_house",0,"pewter_city",5,"True",[1],[5])
newNPC("pewter_speech_house",1,"Moves Guy")
newNPC("pewter_speech_house",2,"Status Effect Tip")

###Pewter Pokemon Center###
newArea("pewter_center","Pewter Pokemon Center",0x3A)
newWarp("pewter_center",0,"pewter_city",6,"True",[1],[6])
newNPC("pewter_center",2,"Gentleman on the Phone")

###Route 3###
newArea("route_3","Route 3",0x0E)
newExit("route_3","pewter_city","has('boulderbadge')")
newExit("route_3","route_4p")
newNPC("route_3",1,"Mt. Moon Traveler")

###Route 4###
#Pewter Side
newArea("route_4p","Route 4 - Pewter Side",0x0F)
newExit("route_4p","route_3")
newWarp("route_4p",0,"mt_moon_center",0)
newWarp("route_4p",1,"mt_moon_1f",0)
newNPC("route_4p",1,"Tripped Over Geodude")
#Cerulean Side
newArea("route_4c","Route 4 - Pewter Side",0x0F)
newWarp("route_4c",1,"mt_moon_b1f",7)
#newExit("route_4c","cerulean_city")
newItemLoc("route_4c",3,"TM 04","TM04")
newHiddenItem("route_4c",0,"Hidden Great Ball","great ball")

###Mt. Moon Pokemon Center###
newArea("mt_moon_center","Mt. Moon Pokemon Center",0x44)
newWarp("mt_moon_center",0,"route_4p",0,"True",[1],[0])
newNPC("mt_moon_center",2,"Six Balls Catcher")
newNPC("mt_moon_center",3,"Newsreading Gentleman")
newNPC("mt_moon_center",4,"Magikarp Salesman")

###Mt. Moon###
#1F
newDungeon("mt_moon_1f","Mt. Moon - 1F",0x3B)
newWarp("mt_moon_1f",0,"route_4p",1,"True",[1],[1])
newWarp("mt_moon_1f",2,"mt_moon_b1f",0,"True",[3,4],[2,3])
newItemLoc("mt_moon_1f",8,"Potion","potion")
newItemLoc("mt_moon_1f",9,"Moon Stone","moon stone")
newItemLoc("mt_moon_1f",10,"Rare Candy","rare candy")
newItemLoc("mt_moon_1f",11,"Escape Rope","escape rope")
newItemLoc("mt_moon_1f",12,"Potion 2","potion")
newItemLoc("mt_moon_1f",13,"TM 12","TM12")
#B1F
newDungeon("mt_moon_b1f","Mt. Moon - B1F",0x3C)
newWarp("mt_moon_b1f",0,"mt_moon_1f",2,"True",[2,3],[3,4])
newWarp("mt_moon_b1f",1,"mt_moon_b2f",0,"True",[4,5,6],[1,2,3])
newWarp("mt_moon_b1f",7,"route_4c",2)
#B2F
newDungeon("mt_moon_b2f","Mt. Moon - B2F",0x3D)
newWarp("mt_moon_b2f",0,"mt_moon_b1f",1,"True",[1,2,3],[4,5,6])
newItemLoc("mt_moon_b2f",6,"Left Fossil","dome fossil")
newItemLoc("mt_moon_b2f",7,"Right Fossil","helix fossil")
newItemLoc("mt_moon_b2f",8,"HP Up","hp up")
newItemLoc("mt_moon_b2f",9,"TM 01","TM01")

for n, a in areas.items():
    print(a)

print("---")

print(canGetToFromStart("museum_back",{"cut","cascadebadge"}))
print(canGetToFromStart("route_4c"))
