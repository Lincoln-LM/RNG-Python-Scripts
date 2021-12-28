from LCRNG import ARNG,ARNGR


class ARNG64(ARNG):
    size = 64

# current deduced group seed
seed = 0x04e2720a
# days since save file creation
days = 3
# set the rng to move backwards
rng = ARNGR(seed)
# +1 for every day since creation
rng.advance(days)
# +1 on save creation
initial_seed = rng.next()
# 64 bit rng seeded with a u32
rng = ARNG64(initial_seed)
# +1 for every day since creation
rng.advance(days)
# +1 on save creation
seed_64 = rng.next()
print(f"Initial Group Seed: {initial_seed:08X}")
print(f"Current u32: {seed:016X}")
print(f"Current u64: {seed_64:016X}")
