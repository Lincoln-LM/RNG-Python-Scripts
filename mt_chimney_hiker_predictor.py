# Script for predicting the Mt. Chimney Hiker in RSE
from LCRNG import PokeRNG

initial_seed = int(input("Initial Seed: 0x"),16)
starting_advances = int(input("Starting Advance: "))
max_advances = int(input("Max Advances: "))
delay = int(input("Delay (mine was 96): "))
rng = PokeRNG(initial_seed)
rng.advance(starting_advances+delay)

sprite = int(input("Sprite (0:Any, 1:Hiker, 2:Camper, 3:Picknicker): "))

sprites = ["Hiker", "Camper", "Picknicker"]

print("Advance, Sprite")
for advance in range(max_advances):
    rval = rng.nextUShort()
    rhiker_check = rval % 64 == 0
    rsprite = (rval % 3)
    check = True
    if not rhiker_check:
        check = False
    if sprite != 0 and rsprite != sprite-1:
        check = False
    if check:
        print(starting_advances+advance,sprites[rsprite],sep=", ")

