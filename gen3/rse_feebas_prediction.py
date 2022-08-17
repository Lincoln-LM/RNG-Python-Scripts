"""
Gen 3 feebas prediction based on a set delay for the feebas rand
"""

from rngs import LCRNG

q = int(input("Searcher/Generator (0/1): "))
f = int(input("Feebass offset (usually 4/5): "))
if q:
    initial_seed = int(input("Initial Seed: 0x"), 16)
    advances = int(input("Advances: "))

    rng = LCRNG.PokeRNG(initial_seed)

    rng.advance(advances)

    seed = rng.seed
    fstring = "Frame " + str(advances-f)
else:
    seed = int(input("Seed: 0x"), 16)
    fstring = "The Frame Before"

rng = LCRNG.PokeRNGR(seed)

rng.advance(f)

high = rng.nextHigh()

if high % 100 < 50:
    print("Feebas Possible! Press A on", fstring)
else:
    print("Feebas is not possible")