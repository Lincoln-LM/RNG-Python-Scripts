"""
Efficiently calculate the distance between two Xoroshiro128+ states
"""
from xoroshiro_jump import compute_jump_polynomial, advance_via_jump
from rngs import Xoroshiro
from poly_jump import *
from mat_recovery import *
from math import ceil, log2, sqrt

def mat_xoroshiro128plus():
    """Create matrix that describes the linear transformation of Xoroshiro128+'s advance function"""
    return np.block([
        [mat_rotl(24) ^ mat_identity() ^ mat_shift(16), mat_identity() ^ mat_shift(16)],
        [mat_rotl(37), mat_rotl(37)]
    ])

def prime_factors(n):
    """Bruteforce all prime factors of n"""
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def distance(start_rng: Xoroshiro.Xoroshiro, end_rng: Xoroshiro.Xoroshiro, cutoff):
    """Efficiently calculate the distance between two Xoroshiro128+ states via Pohlig-Hellman algorithm"""
    advance_matrix = mat_xoroshiro128plus()
    # build a matrix based on start_rng such that jump_poly @ jump_application_mat is equivalent to if you applied the jump polynomial to start_rng
    jump_application_mat = mat_zero(128)
    for i in range(128):
        state = start_rng.state()
        jump_application_mat[i] = tuple((state >> i) & 1 for i in range(128))
        start_rng.next()
    # end_rng @ jump_application_mat_inv = jump_poly to jump from start to end
    jump_application_mat_inv = mat_inverse(jump_application_mat)
    state = end_rng.state()
    jump_poly = (np.array(tuple((state >> i) & 1 for i in range(128)), np.uint8) @ jump_application_mat_inv) % 2

    # build a matrix that describes jumping however many advances are between start and end
    jump_mat = mat_zero(128)
    temp_advance_matrix = mat_identity(128)
    for i in range(128):
        if jump_poly[i]:
            jump_mat ^= temp_advance_matrix
        temp_advance_matrix = (temp_advance_matrix @ advance_matrix) % 2

    primes = prime_factors(2 ** 128 - 1)

    return pohlig_hellman(advance_matrix, jump_mat, primes[:cutoff + 1], 2 ** 128 - 1)

def baby_step_giant_step(_gamma_mat, _h_mat, order):
    """BSGS Algorithm for computing x for _gamma_mat**x = _h_mat in O(sqrt(order)) where order is the order of _gamma_mat under GF(2)"""
    gamma_mat = np.copy(_gamma_mat)
    h_mat = np.copy(_h_mat)

    lookup_table = []
    step_size = ceil(sqrt(order))
    backward_jump_mat = gf2_mat_pow(mat_inverse(gamma_mat), step_size, 128)
    for _ in range(step_size):
        # lookup using hashes
        lookup_table.append(hash(gamma_mat.tobytes()))
        gamma_mat = (gamma_mat @ _gamma_mat) % 2
    for i in range(step_size):
        try:
            j = lookup_table.index(hash(h_mat.tobytes()))
            return i * step_size + j
        except ValueError:
            pass
        h_mat = (h_mat @ backward_jump_mat) % 2
    return None

def chinese_remainder_theorem(mods, remainders):
    """Chinese remainder theorem for solving linear congruences"""
    total = 0
    product = reduce(lambda a, b: a * b, mods)
    for mod, remainder in zip(mods, remainders):
        p = product // mod
        total += remainder * pow(p, -1, mod) * p
    return total % product

def pohlig_hellman(advance_matrix, jump_mat, primes, order):
    """Pohlig-Hellman algorithm optimized for e = 1"""
    remainders = []
    for prime in primes:
        exp = order // prime
        g_i = gf2_mat_pow(advance_matrix, exp, 128)
        h_i = gf2_mat_pow(jump_mat, exp, 128)
        remainders.append(baby_step_giant_step(g_i, h_i, prime))
    return chinese_remainder_theorem(primes, remainders)

if __name__ == "__main__":
    start_rng = Xoroshiro.Xoroshiro(0x1234BEEFDEAD8765, 0x5678DEAD4321BEEF)
    end_rng = Xoroshiro.Xoroshiro(*start_rng.seed.copy())
    advance_via_jump(end_rng, compute_jump_polynomial(0x10008828e513b43d5095b8f76579aa001, 2 ** 24))
    total = 0
    effective_for = 1
    for i, prime in enumerate(prime_factors(2 ** 128 - 1)):
        total += ceil(sqrt(prime))
        effective_for *= prime
        print(f"{i=} {total=} effective for 2**{log2(effective_for)}")
    print()
    print(distance(start_rng, end_rng, 7))
