# script to predict bcc/safari frames and show the spread rerolls

import LCRNG
from tools import getIVs

natures = ['Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive', 'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash', 'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky']

seed = int(input("Seed: 0x"), 16)
start = int(input("Starting Advance: "))
advances = int(input("Advances: "))
bcc = int(input("BCC/Safari (1/0): "))

rng = LCRNG.PokeRNG(seed)
rng.advance(start)

for advance in range(advances):
    go = LCRNG.PokeRNG(rng.seed)
    ivs = [0]*6
    rerolls = 0
    slot = go.nextUShort()
    if bcc:
        go.nextUShort()
    tried = []
    last_advanced = 0
    advanced = 0

    while not 31 in ivs:
        huntnature = go.nextUShort() % 25
        advanced += 1

        while True:
            low = go.nextUShort()
            high = go.nextUShort()
            pid = (high << 16) | low
            nature = pid % 25
            advanced += 2
            if huntnature == nature:
                break

        iv1 = go.nextUShort()
        iv2 = go.nextUShort()
        ivs = getIVs(iv1, iv2)
        advanced += 2

        tried.append(f"{advance+start+last_advanced}, {pid:08X}, {natures[nature].rjust(7)}, {'/'.join(str(iv).zfill(2) for iv in ivs)}")
        last_advanced = advanced
        rerolls += 1
        if rerolls == 4:
            break
    
    print(*tried,sep=" -> ")
    rng.nextUInt()
