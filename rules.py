def ruleEval(rule,inv):
    r = rule.replace(")",",inv)")
    r = r.replace("(,","(") # really hacky fix for rules with one argument lol
    return eval(r)

def has(item,inv):
    return item in inv

def canCut(inv):
    return has("cut",inv) and has("cascadebadge",inv)

def canSurf(inv):
    return has("surf",inv) and has("soulbadge",inv)

def canStrength(inv):
    return has("strength",inv) and has("rainbowbadge",inv)

def canFlash(inv):
    return has("flash",inv) and has("boulderbadge",inv)

def firstSevenBadges(inv):
    return has("boulderbadge",inv) and has("cascadebadge",inv) and has("thunderbadge",inv) and \
           has("rainbowbadge",inv) and has("soulbadge",inv) and has("marshbadge",inv) and \
           has("volcanobadge",inv)

def allBadges(inv):
    return sevenBadges(inv) and has("earthbadge",inv)
