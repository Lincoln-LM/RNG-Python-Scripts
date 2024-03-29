"""
Generate initial seeds based on a target seed and the maximum advances for the target
"""

from rngs import LCRNG

print("------------------------")
maxAdvances = int(input("Max Advances: "))
targetSeed = int(input("Target Seed: 0x"),16)
print("------------------------")

advances = 0
rng = LCRNG.PokeRNGR(targetSeed)
seeds = []
while advances <= maxAdvances:
    rng.next()
    advances += 1
    if rng.seed < 0xFFFF:
        print(advances,hex(rng.seed))
        seeds.append(hex(rng.seed))

print(seeds)
