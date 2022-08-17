"""
Efficiently calculate the distance between two states of generators other than that of the main PRNGs
"""

def xoroshiro_reseed_distance(state0, state1):
    """Efficiently calculate the distance between two states from continous xoroshiro reseeding"""
    mask = 1
    dist = 0

    while state0 != state1:
        if (state0 ^ state1) & mask:
            state0 = (state0 + (0x82A2B175229D6A5B * mask)) & 0xFFFFFFFFFFFFFFFF
            dist += mask
        mask <<= 1

    return dist

def gc_init_seed_distance(state0, state1):
    """Efficiently calculate the distance between two gamecube initial seeds from outdated dolphin"""
    # the lower 5 bits are never modified by tha addition caused by seconds passing
    # if this is not already equal it will never be
    if state0 & 0x1F != state1 & 0x1F:
        return None
    state0 >>= 5
    state1 >>= 5
    mask = 1
    dist = 0

    while state0 != state1:
        if (state0 ^ state1) & mask:
            state0 = (state0 + (1265625 * mask)) & 0x7FFFFFF
            dist += mask
        mask <<= 1

    return dist
