# script for searching for plat resort area magikarp
# im bad at multiprocessing so forgive me
from LCRNG import PokeRNG
from tools import getIVs


def p(seed,vars):
    pressure,target_level,cutecharm,target_natures,target_size,iv_min,iv_max,natures = vars
    if seed % 0x1000000 == 0:
        print(f"{seed/0x28F5C29}% Searched")
    rng = PokeRNG(seed)
    first = rng.nextHigh()
    if first//656 >= 75:
        return
    slot_100 = rng.nextHigh()//656
    if slot_100 != 99:
        return
    level = (rng.nextHigh() % 100) + 1
    if pressure:
        if rng.nextHigh()//0x8000 == 0:
            level = 100
    if level != target_level:
        return
    ccflag = 0
    if cutecharm:
        ccflag = rng.nextHigh()//0x5556
    hunt_nature = rng.nextHigh() // 0xa3e
    if not hunt_nature in target_natures:
        return
    if not ccflag:
        pid = hunt_nature+1
        while pid % 25 != hunt_nature:
            pid = rng.nextHigh() | (rng.nextHigh() << 16)
    else:
        pid = hunt_nature
    ivs = getIVs(rng.nextHigh(), rng.nextHigh())
    for iv in range(6):
        if not iv_min[iv] <= ivs[iv] <= iv_max[iv]:
            return
    # s = 256 * (0xBB ^ (HP * (ATK ^ DEF)) + (0xAA ^ (SPE * (SPA ^ SPDEF)
    size = 0x100 * ((pid&0xFF) ^ ((ivs[0] % 16) * ((ivs[1] % 16) ^ (ivs[2] % 16)))) + ((((pid>>8)&0xFF) ^ ((ivs[5] % 16) * ((ivs[3] % 16) ^ (ivs[4] % 16)))))
    if size != target_size:
        return
    print(f"{seed:08X}, {pid:08X}, {natures[hunt_nature].rjust(7)}, {'/'.join(str(iv).zfill(2) for iv in ivs)} {level:03d} {size:05d}")
if __name__ == "__main__":
    pressure = int(input("Pressure? (1/0):"))
    cutecharm = int(input("Cute Charm Male Lead? (1/0):"))
    target_level = int(input("Level? (1-100):"))
    target_size = int(input("Size? (0-65535):"))
    natures = ['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']
    print(f"Natures: {', '.join(natures)}\n")
    target_natures = [natures.index(x) for x in input("Nature (case sensitive (Jolly,Adamant,Careful)):").split(",")]
    iv_min = [int(iv) for iv in input("IV Min (X/X/X/X/X/X):").split("/")]
    iv_max = [int(iv) for iv in input("IV Max (X/X/X/X/X/X):").split("/")]
    multi = int(input("Multiprocessing? (1/0):"))
    if multi:
        import os
        from multiprocessing import Pool
        from functools import partial
        pp = partial(p,vars=[pressure,target_level,cutecharm,target_natures,target_size,iv_min,iv_max,natures])
        for m in range(0x10):
            pool = Pool(os.cpu_count())
            pool.map(pp, range(m*0x10000000,(m+1)*0x10000000))
    else:
        for seed in range(0x100000000):
            p(seed,[pressure,target_level,cutecharm,target_natures,target_size,iv_min,iv_max,natures])
