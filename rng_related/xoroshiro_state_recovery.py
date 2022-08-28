"""
Recovery of the internal 128 bit state of Xoroshiro128+ via observation of 128 rand(2) outputs

References:
https://github.com/pattirudon/xoroshiroseed-java
https://github.com/niart120/Project_Xe
"""
import numpy as np
from rngs import Xoroshiro
from poly_jump import *
from mat_recovery import *

def mat_xoroshiro128plus():
    """Create matrix that describes the linear transformation of Xoroshiro128+'s advance function"""
    return np.block([
        [mat_rotl(24) ^ mat_identity() ^ mat_shift(16), mat_identity() ^ mat_shift(16)],
        [mat_rotl(37), mat_rotl(37)]
    ])

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

if __name__ == "__main__":
    seed0 = 0x12345678
    seed1 = 0x87654321
    print(f"{seed0=:016X} {seed1=:016X}")

    rng = Xoroshiro.Xoroshiro(seed0, seed1)
    # record 128 observations of rand(2)
    # in SWSH this is done by monitoring the motions of a pokemon on its summary screen
    observations = np.array([[rng.rand(2)] for _ in range(128)], np.uint8)

    # get the inverse of the state-to-observations matrix
    # in order to compute the state from observations
    observations_to_state_mat = mat_inverse(mat_state_to_observations())

    # the first column of ((observations_to_state_mat @ observations) % 2)
    # now contains the bits of the original state
    result = (x[0] for x in ((observations_to_state_mat @ observations) % 2))
    state = reduce(lambda p, q: (int(p) << 1) | int(q), result)

    result_seed0 = state >> 64
    result_seed1 = state & 0xFFFFFFFFFFFFFFFF
    print(f"{result_seed0=:016X} {result_seed1=:016X}")
