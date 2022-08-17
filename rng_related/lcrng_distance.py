"""
Efficiently calculate the distance between two LCRNG states
"""
from lcrng_jump import advance

def distance(state0, state1, mult, add):
    """Efficiently calculate the distance between two LCRNG states"""
    mask = 1
    dist = 0

    while state0 != state1:
        if (state0 ^ state1) & mask:
            # the mult/add used here can be precomputed
            state0 = advance(state0, mask, mult, add)
            dist += mask

        mask <<= 1

    return dist

if __name__ == "__main__":
    from rngs import LCRNG

    print(distance(0, 0xa3561a1, LCRNG.PokeRNG.mult, LCRNG.PokeRNG.add))
