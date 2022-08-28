"""
Recovery of the internal 128 bit state of Xoroshiro128+ via observation of 128 rand(2) outputs

References:
https://github.com/pattirudon/xoroshiroseed-java
https://github.com/niart120/Project_Xe
"""
import numpy as np
from rngs import Xoroshiro
from poly_jump import *

def mat_xoroshiro128plus():
    """Create matrix that describes the linear transformation of Xoroshiro128+'s advance function"""
    return np.block([
        [mat_rotl(24) ^ mat_identity() ^ mat_shift(16), mat_identity() ^ mat_shift(16)],
        [mat_rotl(37), mat_rotl(37)]
    ])

def mat_inverse(mat):
    """Compute the inverse of a matrix via gauss jordan elimination"""
    height, width = mat.shape

    res = np.identity(height, np.uint8)
    pivot = 0
    for i in range(width):
        isfound = False
        for j in range(i, height):
            if mat[j, i]:
                if isfound:
                    mat[j] ^= mat[pivot]
                    res[j] ^= res[pivot]
                else:
                    isfound = True
                    mat[[j, pivot]] = mat[[pivot, j]]
                    res[[j, pivot]] = res[[pivot, j]]
        if isfound:
            pivot += 1

    for i in range(width):
        assert mat[i, i]

    for i in range(1, width)[::-1]:
        for j in range(i)[::-1]:
            if mat[j, i]:
                mat[j] ^= mat[i]
                res[j] ^= res[i]
    return res

def mat_state_to_observations():
    """Create a matrix that represents the transformation of a state to 128 observations"""
    mat = np.identity(128, np.uint8)
    mat_trans = mat_xoroshiro128plus()

    obs = np.zeros((128, 128), np.uint8)
    for i in range(128):
        # 63 is the lowest bit of seed0, 127 is the lowest bit of seed1
        # rand(2) = (seed0 + seed1) & 1
        # therefore:
        # rand(2) = (seed0 & 1) ^ (seed1 & 1)
        obs[i] = mat[63] ^ mat[127]
        # advance the rng
        mat = (mat @ mat_trans) % 2

    return obs

seed0 = 0x12345678
seed1 = 0x87654321
print(f"{seed0=:016X} {seed1=:016X}")

rng = Xoroshiro.Xoroshiro(seed0, seed1)
# record 128 observations of rand(2)
# in SWSH this is done by monitoring the motions of a pokemon on its summary screen
observations = np.array([[rng.rand(2)] for _ in range(128)], np.uint8)

# get the inverse of the state-to-observations matrix in order to compute the state from observations
observations_to_state_mat = mat_inverse(mat_state_to_observations())

result = (x[0] for x in ((observations_to_state_mat @ observations) % 2))
state = reduce(lambda p, q: (int(p) << 1) | int(q), result)

result_seed0 = state >> 64
result_seed1 = state & 0xFFFFFFFFFFFFFFFF
print(f"{result_seed0=:016X} {result_seed1=:016X}")
