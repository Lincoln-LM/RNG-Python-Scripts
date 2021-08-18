# Basic script to path to a target nature in pokewalker pid rng
from MT import MT
from math import ceil
from copy import copy


# Each connection advances mt 192 times
blank_advance = 192

# List of possible natures (no quirky)
natures = ['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful']
print(f"Natures: {', '.join(natures)}\n")

# Get input from the user, target nature, initial seed, iv advance
target_nature = natures.index(input("Nature (case sensitive): "))
seed = int(input("Initial Seed: 0x"),16)
iv_advance = int(input("IV Advance: "))

# Set up MT
rng = MT(seed)

# Simple function to check for target nature, utilizes copy() to avoid having to set up mt again
def check_nature():
    go = copy(rng)
    return go.next() % 24

# Calculate how many connections are 100% needed and how many pokemon will be transferred
transfer_pokemon = iv_advance//2
transfer_connects = ceil(transfer_pokemon/3)
blank_connects = 0

# Advance mt the appropriate amount of times, (192*(needed connections + final connection)) + transferred pokemon
rng.advance((blank_advance * (transfer_connects+1)) + transfer_pokemon)

# Loop through blank connections to find target
while check_nature() != target_nature:
    rng.advance(blank_advance)
    blank_connects += 1

# Print Results
print(f"\n{blank_connects} Blank Connects, after {transfer_connects} Transfer Connects, with {transfer_pokemon} Total Pokemon, PID Advance {(blank_advance * (transfer_connects + blank_connects)) + transfer_pokemon}")
