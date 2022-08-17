# heavily commented script to document how to

def getSeed(hgss,lotto1,lotto2,lotto3):
    reverse_add = 0xFC77A683
    add = 0x3039
    if hgss:
        reverse_add = 0xA3561A1
        add = 0x6073
    lotto1 <<= 16
    for low in range(0x10000):
        # run test seed through LCRNGR to get the original seed
        init = ((lotto1 | low) * 0xEEB9EB65 + reverse_add) & 0xFFFFFFFF
        # advance with ARNG
        seed = (init * 0x6c078965 + 0x1) & 0xFFFFFFFF
        # get next lotto number with seed
        test2 = ((seed * 0x41c64e6d + add) & 0xFFFFFFFF) >> 16
        # if lotto incorrect, continue in loop
        if test2 != lotto2:
            continue
        # advance with ARNG
        seed = (seed * 0x6c078965 + 0x1) & 0xFFFFFFFF
        # get next lotto number with seed
        test3 = ((seed * 0x41c64e6d + add) & 0xFFFFFFFF) >> 16
        # if lotto incorrect, continue in loop
        if test3 != lotto3:
            continue
        # otherwise return original seed
        return init
    # return None if no seed found
    return None
        
# print the hex output of the above function using inputs from the console
print(hex(getSeed(
    int(input("DPPT/HGSS (0/1): ")),
    int(input("Lotto 1: ")), 
    int(input("Lotto 2: ")), 
    int(input("Lotto 3: ")))))