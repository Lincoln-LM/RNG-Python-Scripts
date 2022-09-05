"""
Efficiently jump ahead in the TinyMT sequence
method is described here: http://peteroupc.github.io/jump.html
"""
import numpy as np
from rngs import TinyMT
from sympy import Matrix
from poly_jump import *

def mat_tinymt():
    """Create matrix that describes the linear transformation of TinyMT's shuffle function"""
    state = mat_identity(128)
    state_0 = np.copy(state[:, 0:32])
    state_1 = np.copy(state[:, 32:64])
    state_2 = np.copy(state[:, 64:96])
    state_3 = np.copy(state[:, 96:128])

    y = np.copy(state_3)
    x = np.copy(state_0)
    x[:, 31] = np.zeros((128,)) # & 0x7FFFFFFF
    x ^= state_1 ^ state_2

    x ^= (x @ mat_shift(1, 32)) % 2
    y ^= (((y @ mat_shift(-1, 32)) % 2) ^ x)

    state[:, 0:32] = state_1
    state[:, 32:64] = state_2
    state[:, 64:96] = x ^ ((y @ mat_shift(10, 32)) % 2)
    state[:, 96:128] = y

    for row in range(128):
        if y[row, 0]:
            state[row, 32:96] ^= \
                np.array([(0xfc78ff1f8f7011ee >> i) & 0b1 for i in range(64)], np.uint8)

    return Matrix(state)

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
    characteristic_poly = compute_characteristic_polynomial(mat_tinymt())
    # jump polynomial can be precomputed if the jump count is known ahead of time
    advance_via_jump(rng, compute_jump_polynomial(characteristic_poly, 2**127 - 2))
    print(hex(rng.state[0]), hex(rng.state[1]), hex(rng.state[2]), hex(rng.state[3]))
