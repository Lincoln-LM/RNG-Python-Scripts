"""
Efficiently jump ahead in the LCRNG sequence
"""

def modpow32(a_val, b_val):
    """(uint)(a_val ** b_val)"""
    return pow(a_val, b_val, 0x100000000)

def advance(seed, advances, mult, add):
    """Efficiently jump ahead in the LCRNG sequence"""
    advances_left = advances - 1
    mult_val = mult
    add_val = 1
    add_remainder = 0

    while advances_left > 0:
        if (advances_left & 1) == 0:
            add_remainder += add_val * modpow32(mult_val, advances_left)
            advances_left -= 1
        add_val *= (1 + mult_val)
        mult_val *= mult_val
        advances_left >>= 1

        add_val &= 0xFFFFFFFF
        add_remainder &= 0xFFFFFFFF
        mult_val &= 0xFFFFFFFF

    final_mult = modpow32(mult, advances)
    final_add = ((add_val + add_remainder) * add) & 0xFFFFFFFF
    return (seed * final_mult + final_add) & 0xFFFFFFFF

if __name__ == "__main__":
    from rngs import LCRNG

    print(hex(advance(0, 2**32 - 1, LCRNG.PokeRNG.mult, LCRNG.PokeRNG.add)))
