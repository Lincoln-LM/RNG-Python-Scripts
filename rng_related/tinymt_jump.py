"""
Efficiently jump ahead in the TinyMT sequence
method is described here: http://peteroupc.github.io/jump.html
"""
import numpy as np
from rngs import TinyMT
from sympy import Matrix
from poly_jump import *

# TODO:
# def mat_tinymt():
#     """Create matrix that describes the linear transformation of TinyMT's shuffle function"""
#     return Matrix()

def advance_via_jump(_rng: TinyMT.TinyMT, jump):
    """Apply jump polynomial to rng"""
    seed0 = 0
    seed1 = 0
    seed2 = 0
    seed3 = 0
    for bit in range(mssb_position(jump) + 1):
        if jump & (1 << bit):
            seed0 ^= _rng.state[0]
            seed1 ^= _rng.state[1]
            seed2 ^= _rng.state[2]
            seed3 ^= _rng.state[3]
        _rng.nextState()
    _rng.state = [seed0, seed1, seed2, seed3]

if __name__ == "__main__":
    rng = TinyMT.TinyMT(state = [0x12345678, 0x87654321, 0xDEADBEEF, 0xDBEEAEDF])
    # characteristic polynomial can be precomputed (0x1b0a48045db1bfe951b98a18f31f57486)
    # characteristic_poly = compute_characteristic_polynomial(mat_tinymt())
    characteristic_poly = 0x1b0a48045db1bfe951b98a18f31f57486
    # jump polynomial can be precomputed if the jump count is known ahead of time
    advance_via_jump(rng, compute_jump_polynomial(characteristic_poly, 2**127 - 2))
    print(hex(rng.state[0]), hex(rng.state[1]), hex(rng.state[2]), hex(rng.state[3]))
