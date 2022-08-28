"""
Recovery of the internal 128 bit state of Xoroshiro128+ via observation of 128 rand(2) outputs

References:
https://github.com/pattirudon/xoroshiroseed-java
https://github.com/niart120/Project_Xe
https://github.com/niart120/Project_Xs
"""
import numpy as np
from rngs import Xorshift
from poly_jump import *
from mat_recovery import *

def mat_xorshift128():
    """Create matrix that describes the linear transformation of Xorshift128's advance function"""
    return np.block([
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
    ])

def mat_state_to_observations(intervals, count = 39):
    """
    Create a matrix that represents the transformation of a state to ``count`` observations
    seperated by ``intervals``
    """
    # cut off extra intervals
    intervals = intervals[:count]
    mat = np.identity(128, np.uint8)
    mat_trans = mat_xorshift128()

    obs = np.zeros((4 * count, 128), np.uint8)
    for i in range(count):
        # every second that passes causes a rand(16)
        # if rand(16) in (0, 1): a double blink/single blink happens
        # and is recorded as an observation
        # rand(16) = seed3 & 0xF
        # masking by 0xF is the same as getting the last 4 bits ([-4:])
        obs[4 * i : 4 * (i + 1)] = mat[-4:]
        # intervals are a measure of how many seconds have passed between blinks
        for _ in range(intervals[i]):
            # rng advance for each second in the interval
            mat = (mat @ mat_trans) % 2
    return obs

if __name__ == "__main__":
    seed0 = 0x11223344
    seed1 = 0x55667788
    seed2 = 0x88776655
    seed3 = 0x44332211
    rng = Xorshift.Xorshift(seed0, seed1, seed2, seed3)
    # advance until first blink
    while (rng.seed[3] & 0xF) > 1:
        rng.next()
    seed0, seed1, seed2, seed3 = rng.seed
    print(f"{seed0=:08X} {seed1=:08X} {seed2=:08X} {seed3=:08X}")

    # record 39 observations of blinks
    observations = []
    intervals = []

    for _ in range(39):
        # top 3 bits are always 0 because 0b1 and 0b0 are the only valid blinks
        observations.extend([[0],[0],[0]])
        observations.append([rng.seed[3] & 0xF])
        interval = 1
        rng.next()
        while (rng.seed[3] & 0xF) > 1:
            rng.next()
            interval += 1
        intervals.append(interval)
    observations = np.array(observations, np.uint8)

    # get the inverse of the state-to-observations matrix
    # in order to compute the state from observations
    observations_to_state_mat = mat_inverse(mat_state_to_observations(intervals))

    # the first column of ((observations_to_state_mat @ observations) % 2)
    # now contains the bits of the original state
    result = (x[0] for x in ((observations_to_state_mat @ observations) % 2))
    state = reduce(lambda p, q: (int(p) << 1) | int(q), result)

    result_seed0 = state >> 96
    result_seed1 = (state >> 64) & 0xFFFFFFFF
    result_seed2 = (state >> 32) & 0xFFFFFFFF
    result_seed3 = state & 0xFFFFFFFF
    print(f"{result_seed0=:08X} {result_seed1=:08X} {result_seed2=:08X} {result_seed3=:08X}")
