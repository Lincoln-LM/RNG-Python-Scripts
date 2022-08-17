# script to predict bcc/safari frames and show the spread rerolls

from rngs import LCRNG

def getIVs(iv1, iv2):
    hp = iv1 & 0x1f
    atk = (iv1 >> 5) & 0x1f
    defense = (iv1 >> 10) & 0x1f
    spa = (iv2 >> 5) & 0x1f
    spd = (iv2 >> 10) & 0x1f
    spe = iv2 & 0x1f
    return [ hp, atk, defense, spa, spd, spe ]

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
    slot = go.nextHigh()
    if bcc:
        go.nextHigh()
    tried = []
    last_advanced = 0
    advanced = 0

    while not 31 in ivs:
        huntnature = go.nextHigh() % 25
        advanced += 1

        while True:
            low = go.nextHigh()
            high = go.nextHigh()
            pid = (high << 16) | low
            nature = pid % 25
            advanced += 2
            if huntnature == nature:
                break

        iv1 = go.nextHigh()
        iv2 = go.nextHigh()
        ivs = getIVs(iv1, iv2)
        advanced += 2

        tried.append(f"{advance+start+last_advanced}, {pid:08X}, {natures[nature].rjust(7)}, {'/'.join(str(iv).zfill(2) for iv in ivs)}")
        last_advanced = advanced
        rerolls += 1
        if rerolls == 4:
            break
    
    print(*tried,sep=" -> ")
    rng.next()
