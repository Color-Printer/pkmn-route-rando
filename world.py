from class_defs import *
import random

class World:
    def __init__(self):
        self.areas = {}
        self.inventory = set()
        self.bridge_time = 0
        self.key_item_locs = []
        self.npc_item_locs = []
        self.item_pickups_locs = []
        self.hidden_item_locs = []
        self.allWarps = []
        self.random = random.Random()

    def newArea(self,id,name,map_id,warp_add):
        self.areas[id] = Area(name,id,map_id,warp_add)

    def newTown(self,id,name,map_id,warp_add):
        self.areas[id] = Town(name,id,map_id,warp_add)

    def newDungeon(self,id,name,map_id,warp_add):
        self.areas[id] = Dungeon(name,id,map_id,warp_add)

    def newPokemonCenter(self,id,name,map_id,warp_add):
        self.areas[id] = PokemonCenter(name,id,map_id,warp_add)

    def newExit(self,id,dest_id,req="True"):
        self.areas[id].exits.append(Exit(dest_id,req))

    def newWarp(self,id,w_id,dest_id,dest_w_id,dir,req="True",extra=[],extra_dest=[]):
        x = Warp(id,w_id,dest_id,dest_w_id,dir,req,extra,extra_dest)
        self.areas[id].exits.append(x)
        self.allWarps.append((id,w_id,dir,len(self.areas[id].exits)-1))

    #use this for things that are not actually items, like rescuing mr. fuji
    #or completing silph co
    def newFakeItemLoc(self,id,o_id,name,item,req="True",address=0):
        self.areas[id].objects[o_id] = ItemLocation(item,name,req,address)

    def newItemLoc(self,id,o_id,name,item,req="True",address=0):
        self.areas[id].objects[o_id] = ItemLocation(item,name,req,address)
        self.item_pickups_locs.append(self.areas[id].objects[o_id])

    def newKeyItemLoc(self,id,o_id,name,item,req="True",address=0):
        self.areas[id].objects[o_id] = ItemLocation(item,name,req,address)
        self.key_item_locs.append(self.areas[id].objects[o_id])

    def newNPC(self,id,o_id,name,items=[],req="True"):
        self.areas[id].objects[o_id] = NPC(name,items,req)

    def newHiddenItem(self,id,o_id,name,item,req="True",address=0):
        self.areas[id].hiddenItems[o_id] = ItemLocation(item,name,req,address)
        self.hidden_item_locs.append(self.areas[id].hiddenItems[o_id])

    def clearReachableFlags(self):
        for n, a in self.areas.items():
            a.reachable = False

    def clearVisitedFlags(self):
        for n, a in self.areas.items():
            a.visited = False

    def clearBridgeFlags(self):
        self.clearVisitedFlags()
        for n, a in self.areas.items():
            a.disc = float("Inf")
            a.low = float("Inf")
            a.parent = None

    def canGetFromTo(self,start,goal,i=set()):
        self.clearReachableFlags()
        self.inventory.clear()
        self.inventory.update(i)
        newPlaces = True
        self.areas[start].reachable = True
        while newPlaces == True:
            self.clearVisitedFlags()
            Q = []
            self.areas[start].visited = True
            Q.append(start)
            while len(Q) > 0:
                v = Q.pop()
                if v == goal:
                    return True
                e = self.areas[v].getAllValidExits(self.inventory)
                for w in e:
                    if self.areas[w].visited == False:
                        self.areas[w].visited = True
                        Q.append(w)
            newPlaces = False
            numItems = len(self.inventory)
            for n, a in self.areas.items():
                if a.visited == True:
                    if a.reachable == False:
                        newPlaces = True
                        a.reachable = True
                    a.getAllItems(self.inventory)
            if len(self.inventory) > numItems:
                newPlaces = True
        return self.areas[goal].reachable

    def canGetToFromStart(self,goal,i=set()):
        return self.canGetFromTo("reds_house_2F",goal,i)


    def bridgeHelper(self,node):
        node.visited = True
        node.disc = self.bridge_time
        node.low = self.bridge_time
        self.bridge_time += 1

        edges = node.getAllGraphConnections()
        for e in edges:
            other_end = self.areas[e]
            if other_end.visited == False:
                other_end.parent = node
                self.bridgeHelper(other_end)
                node.low = min(node.low,other_end.low)
                if other_end.low > node.disc:
                    print(node.name + " - " + other_end.name)
            elif other_end != node.parent:
                node.low = min(node.low,other_end.disc)

    def findBridges(self):
        self.clearBridgeFlags()
        self.bridge_time = 0
        for n, a in self.areas.items():
            if a.visited == False:
                self.bridgeHelper(a)

    def allPhysicallyConnected(self):
        x = True
        self.clearVisitedFlags()
        Q = []
        self.areas["reds_house_2F"].visited = True
        Q.append("reds_house_2F")
        while len(Q) > 0:
            v = Q.pop()
            e = self.areas[v].getAllGraphConnections()
            for w in e:
                if self.areas[w].visited == False:
                    self.areas[w].visited = True
                    Q.append(w)
        for n, a in self.areas.items():
            if a.visited == False:
                x = False
        return x

    def onePokemonCenter(self,area):
        pc = 0
        for x in self.areas[area].exits:
            if isinstance(self.areas[x.destination],PokemonCenter) and x.requirements == "True":
                pc += 1
        if pc == 1:
            return True
        else:
            return False

    def checkPokemonCenters(self):
        for n, a in self.areas.items():
            if isinstance(a,Town) and self.onePokemonCenter(n)==False:
                return False
        return True

    def shuffle_items(self,flags):
        item_mapping = {}

        r_keyItems = False
        r_npcItems = False
        r_pickItems = False
        r_hiddenItems = False
        for s in flags:
            pool = []
            if "K" in s and r_keyItems == False:
                pool += self.key_item_locs
                r_keyItems = True
            if "N" in s and r_npcItems == False:
                pool += self.npc_item_locs
                r_npcItems = True
            if "I" in s and r_pickItems == False:
                pool += self.item_pickups_locs
                r_pickItems = True
            if "H" in s and r_hiddenItems == False:
                pool += self.hidden_item_locs
                r_hiddenItems = True
            initialOrder = pool[:]
            self.random.shuffle(initialOrder)
            mapping = dict(zip(pool, initialOrder))
            item_mapping.update(mapping)

        return item_mapping

    def shuffle_warps(self,flags):
        warp_mapping = {}

        north_exits = []
        south_exits = []
        west_exits = []
        east_exits = []
        stair_exits = []
        for w in self.allWarps:
            if w[2] == "north":
                north_exits.append(w)
            elif w[2] == "south":
                south_exits.append(w)
            elif w[2] == "east":
                east_exits.append(w)
            elif w[2] == "west":
                west_exits.append(w)
            elif w[2] == "stairs":
                stair_exits.append(w)
        self.random.shuffle(stair_exits)
        while len(north_exits) != len(south_exits):
            if len(north_exits) > len(south_exits):
                south_exits.append(stair_exits.pop())
            else:
                north_exits.append(stair_exits.pop())
        while len(west_exits) != len(east_exits):
            if len(west_exits) > len(east_exits):
                east_exits.append(stair_exits.pop())
            else:
                west_exits.append(stair_exits.pop())
        x = int(len(stair_exits)/2)
        for i in range(x):
            n = self.random.randint(1,2)
            if n == 1:
                north_exits.append(stair_exits.pop())
                south_exits.append(stair_exits.pop())
            else:
                west_exits.append(stair_exits.pop())
                east_exits.append(stair_exits.pop())
        self.random.shuffle(north_exits)
        self.random.shuffle(south_exits)
        self.random.shuffle(west_exits)
        self.random.shuffle(east_exits)
        warp_mapping = dict(zip(north_exits, south_exits))
        warp_mapping.update(dict(zip(west_exits, east_exits)))

        for w1,w2 in warp_mapping.items():
            self.areas[w1[0]].exits[w1[3]].destination = w2[0]
            self.areas[w1[0]].exits[w1[3]].dest_id = self.areas[w2[0]].mapid
            self.areas[w1[0]].exits[w1[3]].dest_warp_id = w2[1]
            self.areas[w2[0]].exits[w2[3]].destination = w1[0]
            self.areas[w2[0]].exits[w2[3]].dest_id = self.areas[w1[0]].mapid
            self.areas[w2[0]].exits[w2[3]].dest_warp_id = w1[1]

        return warp_mapping
