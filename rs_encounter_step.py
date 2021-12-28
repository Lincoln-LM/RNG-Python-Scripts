from LCRNG import PokeRNG
from tools import getIVs


natures = ['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
compatabilities = [20,50,70]
methods = {1:(0,0),2:(1,0),4:(0,1)}

# edit
initial_seed = 0x5A0 # initial seed
initial_advances = 0 # starting advances
max_advances = 1000 # total advances to show
compatability = 0 # 0: dont, 1: get along, 2: very well
method = 1 # 1/2/4
rate = 13 # ? get from the rom for your location
show_non_encounter = False # whether or not to show lows with no encounters
# ----

rng = PokeRNG(initial_seed)
rng.advance(initial_advances)

for cnt in range(max_advances):
    go = PokeRNG(rng.seed)
    if go.nextHigh() * 100 // 0xFFFF < compatabilities[compatability]:
        low = go.nextHigh() % 0xfffe + 1
        if go.nextHigh() % 2880 < rate*16:
            go.advance(2) # encounter slot
            
            search_nature = go.nextHigh() % 25
            pid = -1
            while pid % 25 != search_nature:
                low = go.nextHigh()
                high = go.nextHigh()
                pid = (high << 16) | low

            go.advance(methods[method][0])
            iv1 = go.nextHigh()
            go.advance(methods[method][1])
            iv2 = go.nextHigh()
            ivs = getIVs(iv1,iv2)
        
            print(f"{initial_advances+cnt} {low:04X} {pid:08X} {natures[search_nature]} {'/'.join(str(iv) for iv in ivs)}")
        elif show_non_encounter:
            print(f"{initial_advances+cnt} {low:04X} No Encounter")
    rng.next()
