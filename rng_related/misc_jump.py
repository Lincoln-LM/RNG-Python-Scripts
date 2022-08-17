"""
Efficiently jumping ahead in sequences other than that of the main PRNGs
"""

def xoroshiro_reseed_jump(seed, jump_count):
    """Jump ahead in a sequence of continous xoroshiro reseeding"""
    # continuous reseeding is equivalent to adding 0x82A2B175229D6A5B each reseed
    return (seed + 0x82A2B175229D6A5B * jump_count) & 0xFFFFFFFFFFFFFFFF

def gc_init_seed_jump(seed, jump_count):
    """Jump ahead in the sequence of gamecube initial seeds that outdated dolphin gives"""
    # every second adds 40500000 to the seed
    return (seed + 40500000 * jump_count) & 0xFFFFFFFF
