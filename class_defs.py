import rules

class Area:
    def __init__(self,name,identifier,mapid,warp_add):
        self.name = name
        self.id = identifier
        self.mapid = mapid
        self.exits = []
        self.objects = {}
        self.hiddenItems = {}
        self.warpAddresses = warp_add

    def canUseExit(self,exitNum,items):
        return self.exits[exitNum].canUse(items)

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

    def getAllValidExits(self,items):
        v = []
        for x in self.exits:
            if x.canUse(items) and x.destination not in v:
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

    def canUse(self,items):
        return rules.ruleEval(self.requirements,items)

class Warp(Exit):
    def __init__(self,home,warp_id,dest_id,dest_warp_id,direction,req="True",extra=[],extra_dest=[]):
        super().__init__(dest_id,req)
        self.home = home
        self.warp_id = warp_id
        self.extra_warp_id = extra
        self.dest_warp_id = dest_warp_id
        self.extra_dest_warp_id = extra_dest
        self.direction = direction

class ItemLocation:
    def __init__(self,item,name,req="True",address=0):
        self.item = item
        self.requirements = req
        self.name = name
        self.address = address

    def __str__(self):
        s = self.name + ": " + self.item
        if self.requirements != "True":
            s = s + " - Requirements: " + self.requirements
        return s

    def canAccess(self,items):
        return rules.ruleEval(self.requirements,items)

    def get(self,items):
        if self.canAccess(items):
            items.add(self.item)

class HiddenItem(ItemLocation):
    def canAccess(self,items):
        return rules.ruleEval(self.requirements + " and has('itemfinder')",items)

class NPC:
    def __init__(self,name,items=[],req="True"):
        self.name = name
        self.itemsHeld = items
        self.requirements = req

    def canAccess(self,items):
        return rules.ruleEval(self.requirements,items)

    def getItems(self,items):
        if self.canAccess(items):
            for i in self.itemsHeld:
                i.get(items)
