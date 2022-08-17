"""
Efficiently jump ahead in the Xorshift128+ sequence
method is described here: http://peteroupc.github.io/jump.html
"""
import numpy as np
from rngs import Xorshift
from sympy import Matrix
from poly_jump import *

def mat_xorshift128plus():
    """Create matrix that describes the linear transformation of Xorshift128+'s advance function"""
    return Matrix(np.block([
        [mat_zero(32),
         mat_identity(32),
         mat_zero(32),
         mat_zero(32)
        ],
        [mat_zero(32),
         mat_zero(32),
         mat_identity(32),
         mat_zero(32)
        ],
        [mat_zero(32),
         mat_zero(32),
         mat_zero(32),
         mat_identity(32)
        ],
        [(mat_identity(32) ^ mat_shift(-8, 32)) @ (mat_identity(32) ^ mat_shift(11, 32)) % 2,
         mat_zero(32),
         mat_zero(32),
         mat_identity(32) ^ mat_shift(-19, 32)
        ],
    ]))

def advance_via_jump(_rng: Xorshift.Xorshift, jump):
    """Apply jump polynomial to rng"""
    # as per https://xoshiro.di.unimi.it/xorshift128plus.c
    seed0 = 0
    seed1 = 0
    seed2 = 0
    seed3 = 0
    for bit in range(128):
        if jump & (1 << bit):
            seed0 ^= _rng.seed[0]
            seed1 ^= _rng.seed[1]
            seed2 ^= _rng.seed[2]
            seed3 ^= _rng.seed[3]
        _rng.next()
    _rng.seed = [seed0, seed1, seed2, seed3]

if __name__ == "__main__":
    rng = Xorshift.Xorshift(0x12345678, 0x87654321, 0x87654321, 0x12345678)
    # characteristic polynomial can be precomputed (0x1000000010046d8b3f985d65ffd3c8001)
    characteristic_poly = compute_characteristic_polynomial(mat_xorshift128plus())
    # jump polynomial can be precomputed if the jump count is known ahead of time
    advance_via_jump(rng, compute_jump_polynomial(characteristic_poly, 2**128 - 2))
    print(hex(rng.seed[0]), hex(rng.seed[1]), hex(rng.seed[2]), hex(rng.seed[3]))
