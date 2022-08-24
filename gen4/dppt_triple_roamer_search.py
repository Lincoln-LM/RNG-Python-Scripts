"""
Search for seeds that will provide triple shiny roamers using z3
"""

import z3
from rngs import LCRNG

def sym_pokerng(_seed):
    """Sym function for LCRNG.PokeRNG.next()"""
    # limited to 32 bits already, no need for & 0xFFFFFFFF
    return _seed * LCRNG.PokeRNG.mult + LCRNG.PokeRNG.add

solver = z3.Solver()
seed = z3.BitVecs('seed', 32)[0]
sym_seed = seed
sym_seed = sym_pokerng(sym_seed)

# Condsidering that:
# pid = rng.nextHigh() | (rng.nextHigh() >> 16)
# psv = (pid & 0xFFFF) ^ (pid >> 16)
# Calculating psv can be simplified down to (rng.nextHigh() ^ rng.nextHigh()) >> 3
# and further to rng.nextHigh(13) ^ rng.nextHigh(13)
# rng.nextHigh(13) is the same as seed >> 19 (as 32 - 13 = 19)
psv0 = sym_seed >> 19
sym_seed = sym_pokerng(sym_seed)
psv0 ^= sym_seed >> 19

# 3 + 1 advances because there is a gap of 3 and also the advance thats actually used in pid
for _ in range(3 + 1):
    sym_seed = sym_pokerng(sym_seed)

psv1 = sym_seed >> 19
sym_seed = sym_pokerng(sym_seed)
psv1 ^= sym_seed >> 19

for _ in range(3 + 1):
    sym_seed = sym_pokerng(sym_seed)

psv2 = sym_seed >> 19
sym_seed = sym_pokerng(sym_seed)
psv2 ^= sym_seed >> 19

solver.add(z3.And(psv0 == psv1, psv0 == psv2))

# while there is still a possible result
while solver.check() == z3.sat:
    model = solver.model()
    found_seed = model[seed].as_long()
    rng = LCRNG.PokeRNG(found_seed)
    psv0 = rng.nextHigh(13) ^ rng.nextHigh(13)
    rng.advance(3)
    psv1 = rng.nextHigh(13) ^ rng.nextHigh(13)
    rng.advance(3)
    psv2 = rng.nextHigh(13) ^ rng.nextHigh(13)
    print(f"{found_seed=:08X} {psv0=} {psv1=} {psv2=}")
    # make current result invalid as to find others
    solver.add(seed != model[seed])
