from items import *

def ruleEval(rule,inv):
    r = rule.replace(")",",inv)")
    r = r.replace("(,","(") # really hacky fix for rules with one argument lol
    return eval(r)

def has(item,inv):
    return item in inv

def canCut(inv):
    return has(CUT,inv) and (has(CASCADEBADGE,inv) or has("free_hms",inv))

def canSurf(inv):
    return has(SURF,inv) and (has(SOULBADGE,inv) or has("free_hms",inv)) and canFishGood(inv)

def canStrength(inv):
    return has(STRENGTH,inv) and (has(RAINBOWBADGE,inv) or has("free_hms",inv))

def canFlash(inv):
    return has(FLASH,inv) and (has(BOULDERBADGE,inv) or has("free_hms",inv))

def firstSevenBadges(inv):
    return has(BOULDERBADGE,inv) and has(CASCADEBADGE,inv) and has(THUNDERBADGE,inv) and \
           has(RAINBOWBADGE,inv) and has(SOULBADGE,inv) and has(MARSHBADGE,inv) and \
           has(VOLCANOBADGE,inv)

def allBadges(inv):
    return firstSevenBadges(inv) and has(EARTHBADGE,inv)

def canFishGood(inv):
    return has(GOOD_ROD,inv) or has(SUPER_ROD,inv)
