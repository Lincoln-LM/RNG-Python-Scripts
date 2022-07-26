"""Reversing Primo's password protected eggs in HGSS"""

def forward_aikotoba(words):
    """Calculate what egg to give and what tid is needed for said egg"""
    out = [words[0] & 0xFF, -1, -1, -1]

    for i in range(1,4):
        if words[i] < words[i - 1]:
            val = 351 - (words[i - 1] - words[i])
            if 0xFF < val:
                return None
            out[i] = val
        else:
            out[i] = (words[i] - words[i - 1]) & 0xFF

    for _ in range(5):
        low = out[3] & 1
        for i in range(3, 0, -1):
            out[i] = (((out[i - 1] & 1) << 7) | (out[i] >> 1))
        out[0] = ((low << 7) | (out[0] >> 1)) & 0xFF

    last = out[3]
    for i in range(0,3):
        out[i] ^= (last & 0xF0) | (last >> 4)

    for _ in range(last & 0xF):
        low = out[2] & 1
        for i in range(2, 0, -1):
            out[i] = (((out[i - 1] & 1) << 7) | (out[i] >> 1))
        out[0] = ((low << 7) | (out[0] >> 1)) & 0xFF
    species = out[0] & 0xF - 8
    tid = ((out[1] ^ out[0]) << 8) | (out[2] ^ out[0])
    if 0 <= species <= 2 and out[3] == ((out[2] ^ out[0]) * (out[0] + (out[1] ^ out[0])) & 0xFF):
        return species, tid
    return None

def reverse_aikotoba(species, tid):
    """Reverse to get the needed passphrase from species and tid"""
    # valid species values are in the range [8,10]
    species_val = species + 8
    tid_high = tid >> 8
    tid_low = tid & 0xFF
    # reverse `species = out[0] & 0xF - 8`
    # high nibble of out[0] is always 6
    out_0 = species_val | (0x6 << 4)
    # reverse `tid = ((out[1] ^ out[0]) << 8) | (out[2] ^ out[0])`
    out_1 = tid_high ^ out_0
    out_2 = tid_low ^ out_0
    # out_3 must be this for it to be valid
    out_3 = ((out_2 ^ out_0) * (out_0 + (out_1 ^ out_0)) & 0xFF)
    out = [out_0, out_1, out_2, out_3]
    cycles = out[3] & 0xF
    xor_val = (out[3] >> 4) | (out[3] & 0xF0)
    for _ in range(cycles):
        out_2_low = out[0] >> 7
        # information is lost here but its added back later via out_2_low
        out[0] <<= 1
        out[0] &= 0xFF
        for i in range(1,3):
            out[i - 1] |= out[i] >> 7
            out[i] <<= 1
            out[i] &= 0xFF
        out[2] |= out_2_low
    for i in range(3):
        out[i] ^= xor_val
    for _ in range(5):
        out_3_low = out[0] >> 7
        # information is lost here but its added back later via out_3_low
        out[0] <<= 1
        out[0] &= 0xFF
        for i in range(1,4):
            out[i - 1] |= out[i] >> 7
            out[i] <<= 1
            out[i] &= 0xFF
        out[3] |= out_3_low
    # inverse of `out = [words[0] & 0xFF, -1, -1, -1]`
    words = [out[0], -1, -1, -1]
    for i in range(1, 4):
        # there are only 351 words to choose from
        words[i] = (words[i - 1] + out[i]) % 351
    return words
