# Used to get seed from PID/IVs

def recoverLower16BitsPID(pid):
    low = []
    flags = []

    for _ in range(0x10000):
        low.append(0)
        flags.append(False)

    k = 0xC64E6D00
    mult = 0x41c64e6d
    add = 0x6073

    for i in range(256):
        right = (mult * i + add) & 0xFFFFFFFF
        val = (right >> 16) & 0xFFFF
        flags[val] = True
        low[val] = i & 255
        val -= 1
        flags[val] = True
        low[val] = i & 255

    first = (pid << 16) & 0xFFFFFFFF
    second = pid & 0xFFFF0000
    search = (second - (first * mult)) & 0xFFFFFFFF
    origin = []
    for i in range(256):
        if flags[search >> 16]:
            test = first | (i << 8) | low[search >> 16]
            if ((test * mult + add) & 0xffff0000) == second:
                origin.append(test)
        search = (search-k) & 0xFFFFFFFF
    
    return origin

def recoverLower16BitsIV(hp, atk, defe, spa, spd, spe):
    low = []
    flags = []

    for _ in range(0x10000):
        low.append(0)
        flags.append(False)

    k = 0xC64E6D00
    mult = 0x41c64e6d
    add = 0x6073

    for i in range(256):
        right = (mult * i + add) & 0xFFFFFFFF
        val = (right >> 16) & 0xFFFF
        flags[val] = True
        low[val] = i & 255
        val -= 1
        flags[val] = True
        low[val] = i & 255

    first = (((hp | (atk << 5) | (defe << 10)) << 16)) & 0xFFFFFFFF
    second = (((spe | (spa << 5) | (spd << 10)) << 16)) & 0xFFFFFFFF

    search1 = (second - (first * mult)) & 0xFFFFFFFF
    search2 = (second - ((first ^ 0x80000000) * mult)) & 0xFFFFFFFF


    origin = []
    for i in range(256):
        if flags[search1 >> 16]:
            test = first | (i << 8) | low[search1 >> 16]
            if ((test * mult + add) & 0x7fff0000) == second:
                origin.append(test)

        if flags[search2 >> 16]:
            test = first | (i << 8) | low[search2 >> 16]
            if ((test * mult + add) & 0x7fff0000) == second:
                origin.append(test)
        
        search1 = (search1-k) & 0xFFFFFFFF
        search2 = (search2-k) & 0xFFFFFFFF
    
    return origin