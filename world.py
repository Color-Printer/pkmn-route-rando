from class_defs import *

class World:
    def __init__(self):
        self.areas = {}
        self.inventory = set()
        self.bridge_time = 0

    def newArea(self,id,name,map_id):
        self.areas[id] = Area(name,id,map_id)

    def newTown(self,id,name,map_id):
        self.areas[id] = Town(name,id,map_id)

    def newDungeon(self,id,name,map_id):
        self.areas[id] = Dungeon(name,id,map_id)

    def newExit(self,id,dest_id,req="True"):
        self.areas[id].exits.append(Exit(dest_id,req))

    def newWarp(self,id,w_id,dest_id,dest_w_id,req="True",extra=[],extra_dest=[]):
        self.areas[id].exits.append(Warp(w_id,dest_id,dest_w_id,req,extra,extra_dest))

    def newItemLoc(self,id,o_id,name,item,req="True"):
        self.areas[id].objects[o_id] = ItemLocation(item,name,req)

    def newNPC(self,id,o_id,name,items=[],req="True"):
        self.areas[id].objects[o_id] = NPC(name,items,req)

    def newHiddenItem(self,id,o_id,name,item,req="True"):
        self.areas[id].hiddenItems[o_id] = ItemLocation(item,name,req)

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
