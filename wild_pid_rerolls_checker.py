# Script to check pid rerolls for a frame

import LCRNG
from tools import getIVs

natures = [ "Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky" ]
methods = {1:(0,0),2:(1,0),4:(0,1)}

def getWild(seed,m):
    go = LCRNG.PokeRNG(seed)
    
    go.nextUInt()
    go.nextUInt()
    go.nextUInt()
    
    searchNature = go.nextUShort() % 25
    pidcheck = True
    rerolls = -1
    while pidcheck:
        low = go.nextUShort()
        high = go.nextUShort()
        pid = (high << 16) | low
        pidcheck = pid % 25 != searchNature
        rerolls += 1
    go.advance(m[0])
    iv1 = go.nextUShort()
    go.advance(m[1])
    iv2 = go.nextUShort()
    ivs = getIVs(iv1,iv2)
    return [hex(pid),natures[searchNature],ivs, rerolls]

while True:
    seed = int(input("Initial Seed: 0x"),16)
    frame = int(input("Frame: "))
    rng = LCRNG.PokeRNG(seed)
    rng.advance(frame-1)
    for m in methods:
        info = getWild(rng.seed,methods[m])
        print("Method",m,info[0][2:],info[1],info[2])
    print("Rerolls:", info[3])
    print()
    
