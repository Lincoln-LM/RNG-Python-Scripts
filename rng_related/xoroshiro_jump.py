"""
Efficiently jump ahead in the Xoroshiro128+ sequence
method is described here: http://peteroupc.github.io/jump.html
"""
import numpy as np
from rngs import Xoroshiro
from sympy import Matrix
from poly_jump import *

def mat_xoroshiro128plus():
    """Create matrix that describes the linear transformation of Xoroshiro128+'s advance function"""
    return Matrix(np.block([
        [mat_rotl(24) ^ mat_identity() ^ mat_shift(16), mat_identity() ^ mat_shift(16)],
        [mat_rotl(37), mat_rotl(37)]
    ]))

def advance_via_jump(_rng: Xoroshiro.Xoroshiro, jump):
    """Apply jump polynomial to rng"""
    # as per https://xoshiro.di.unimi.it/xoroshiro128plus.c
    seed0 = 0
    seed1 = 0
    for bit in range(mssb_position(jump) + 1):
        if jump & (1 << bit):
            seed0 ^= _rng.seed[0]
            seed1 ^= _rng.seed[1]
        _rng.next()
    _rng.seed = [seed0, seed1]

if __name__ == "__main__":
    rng = Xoroshiro.Xoroshiro(0x1234567887654321, 0x8765432112345678)
    # characteristic polynomial can be precomputed (0x10008828e513b43d5095b8f76579aa001)
    characteristic_poly = compute_characteristic_polynomial(mat_xoroshiro128plus())
    # jump polynomial can be precomputed if the jump count is known ahead of time
    advance_via_jump(rng, compute_jump_polynomial(characteristic_poly, 2**128 - 2))
    print(hex(rng.seed[0]), hex(rng.seed[1]))
