"""
Reverse the LCRNG sequence via a LCRNG with new different mult/add
"""

def modpow32(a_val, b_val):
    """(uint)(a_val ** b_val)"""
    return pow(a_val, b_val, 0x100000000)

def reverse(mult, add):
    """Reverse the LCRNG sequence via a LCRNG with new different mult/add"""
    # modular multiplicative inverse
    reverse_mult = modpow32(mult, -1)
    reverse_add = ((-add * reverse_mult) & 0xFFFFFFFF)
    return reverse_mult, reverse_add

if __name__ == "__main__":
    from rngs import LCRNG

    print(*(hex(x) for x in reverse(LCRNG.PokeRNG.mult, LCRNG.PokeRNG.add)))
