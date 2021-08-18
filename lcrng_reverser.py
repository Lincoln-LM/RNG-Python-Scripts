# Script to find the reverse of an LCRNG
# if b = (a * mult + add) & 0xFFFFFFFF then (b * reverse_mult + reverse_add) & 0xFFFFFFFF = a

# extended euclids algorithm thing to get your reverse mult
def find_reverse_mult(mult, limit): 
    if mult == 0:
        return 0,1
    x1,y1 = find_reverse_mult(limit%mult, mult)
    x = y1 - (limit//mult) * x1
    y = x1
    
    return x,y

# simple way to find the reverse add, this effectively subtracts the normal add after being multiplied by the reverse_mult
def find_reverse_add(add,reverse_mult):
    return ((-add * reverse_mult) & 0xFFFFFFFF)

add = int(input("add: 0x"),16)
mult = int(input("mult: 0x"),16)

reverse_mult, _ = find_reverse_mult(mult, 0x100000000)
reverse_mult &= 0xFFFFFFFF
reverse_add = find_reverse_add(add, reverse_mult)

print(f"reverse_mult: 0x{reverse_mult:08X}, reverse_add: 0x{reverse_add:08X}")