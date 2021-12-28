# Script to get Gen 4 initial seeds from a target seed

import LCRNG

def seedchecker4(seed,year,message=True):
    if year < 2000 or year > 2099:
        if message:
            print("Please Enter a year between 2000 and 2099")
        return [False,0]
    
    ab = seed >> 24
    cd = (seed >> 16) & 0xFF
    efgh = seed & 0xFFFF

    delay = (efgh + (2000 - year)) & 0xFFFF
    hour = cd

    if hour > 23:
        if message:
            print("Seed is invalid. Please enter a valid seed.")
        return [False,0]
    
    return [True,delay]

done = False
print("Initial Seed Finder")

print("---------------------")
targetSeed = int(input("Target Seed: 0x"),16)
minDelay = int(input("Min Delay: "))
maxDelay = int(input("Max Delay: "))
print("---------------------")

print("Advances, Seed, Delay")
rng = LCRNG.PokeRNGR(targetSeed)
advances = 0

while not done:
    sc = seedchecker4(rng.seed,2000,False)
    while not sc[0] or sc[1] >= maxDelay or sc[1] <= minDelay:
        rng.next()
        advances += 1
        sc = seedchecker4(rng.seed,2000,False)
    print(advances, hex(rng.seed), seedchecker4(rng.seed,2000,False)[1])
    ch = input("Next? (y/n): ")
    if ch.lower() != "y":
        done = True
    else:
        rng.next()
        advances += 1