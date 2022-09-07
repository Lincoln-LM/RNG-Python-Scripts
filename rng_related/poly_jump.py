"""
Functions that aid in efficiently jumping ahead GF(2)-linear PRNGS
method is described here: http://peteroupc.github.io/jump.html
"""
from functools import reduce
import numpy as np

def mat_zero(size = 64):
    """Zero matrix of size"""
    return np.zeros((size, size), dtype = "uint8")

def mat_identity(size = 64):
    """Identity matrix of size"""
    return np.identity(size, dtype = "uint8") 

def mat_rotl(n, size = 64):
    """Rolled identity matriz of size rolled by -n"""
    return np.roll(mat_identity(size), -n, axis = 0)

def mat_shift(n, size = 64):
    """Eye matrix of size at position n"""
    return np.eye(size, k = n, dtype = "uint8")

def compute_characteristic_polynomial(mat):
    """Compute the characteristic polynomial of a transformation matrix in the field GF(2))"""
    return reduce(lambda p, q: (p << 1) | (q & 1), mat.charpoly().all_coeffs())

def mssb_position(polynomial):
    """Get the position of the most significant set bit in polynomial"""
    result = -1
    while polynomial != 0:
        polynomial >>= 1
        result += 1
    return result

def bit_mod_gf2(polynomial, modulus, last_bit_pos = 128):
    """Compute polynomial % modulus in the field GF(2)"""
    # if the mssb of modulus is higher than polynomial: return polynomial
    if polynomial >> last_bit_pos == 0:
        return polynomial
    poly_mssb = mssb_position(polynomial >> last_bit_pos) + last_bit_pos
    shift_num = poly_mssb - last_bit_pos
    # print(shift_num)
    # line up mssb
    modulus <<= shift_num
    # only go until modulus is back at its original value
    for shift_pos in range(shift_num + 1):
        # divides perfectly before last xor
        if polynomial == 0:
            return 0
        # if modulus "fits" at this position: polynomial ^= shifted modulus
        if polynomial >> (poly_mssb - shift_pos) == 1:
        # if polynomial >> mssb_position(modulus) == 1:
            polynomial ^= modulus
        # check next position
        modulus >>= 1
    # remainder is left in polynomial
    return polynomial

def bit_multmod_gf2(multiplicand, multiplier, modulus = None, size = 256, last_bit_pos = 128):
    """Calculate multiplicand * multiplier in the field GF(2)"""
    result = 0
    current_bit = 0
    mask = 2 ** size - 1
    modulus = modulus or mask + 1
    # if either are 0, there is nothing left to do
    while 0 not in (multiplicand, multiplier):
        # multiply 1 bit at a time
        result ^= multiplicand * (multiplier & 1)
        multiplicand <<= 1
        multiplier >>= 1
        # bits outside of the mask wont be included in final result
        multiplicand &= mask
        current_bit += 1
    return bit_mod_gf2(result, modulus, last_bit_pos)

def bit_base2_powmod_gf2(power, modulus, size = 256, last_bit_pos = 128):
    """Calculate 2 ** power % modulus in the field GF(2)"""
    base = 2
    result = 1
    # exponentiation by squares
    while power > 0:
        if power & 1:
            result = bit_multmod_gf2(result, base, modulus, size, last_bit_pos)

        power >>= 1
        base = bit_multmod_gf2(base, base, modulus, size, last_bit_pos)
    return result

def compute_jump_polynomial(characteristic_polynomial, jump_count, size = 256, last_bit_pos = 128):
    """Compute jump polynomial from characteristic polynomial and the distance to jump"""
    return bit_base2_powmod_gf2(jump_count, characteristic_polynomial, size, last_bit_pos)
