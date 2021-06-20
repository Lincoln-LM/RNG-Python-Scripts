# Script to display jirachis you can hit

import LCRNG

natures = ['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

# Working backwards this validates if a Jirachi seed is obtainable
# There are 3 different patterns for this (6/7/8 advances) plus menu checking
def validate_jirachi(seed):
    rng = LCRNG.XDRNGR(seed)

    num1 = rng.nextUShort()
    num2 = rng.nextUShort()
    num3 = rng.nextUShort()

    rng.advance(3)
    if (num1 <= 0x4000): # 6 advances
        if (validate_menu(rng.seed)):
            return True

    rng.advance(1)
    if (num2 > 0x4000 and num1 <= 0x547a): # 7 advances
        if (validate_menu(rng.seed)):
            return True

    rng.advance(1)
    if (num3 > 0x4000 and num2 > 0x547a): # 8 advances
        if (validate_menu(rng.seed)):
            return True

    return False

# Working backwards from a seed check if the menu sequence will end on said seed
# Menu will advance the prng until it collects a 1, 2, and 3
def validate_menu(seed):
    mask = 0
    target = seed >> 30

    # Impossible to stop 0
    if (target == 0):
        return False
    else:
        mask |= 1 << target

    rng = LCRNG.XDRNGR(seed)
    while ((mask & 14) != 14):
        num = rng.nextUInt() >> 30

        # Basically this check means that while rolling for 1, 2, and 3
        # We hit our original target meaning that we can't land on the target
        if (num == target):
            return False

        mask |= 1 << num

    return True
seed = 0x3B03D5CF
rng = LCRNG.XDRNG(seed)
print(f"{seed:X}")
print("Advance, Seed, Shiny, SID, PID, Nature, IVs")
for advance in range(100):
    if validate_jirachi(rng.seed):
        filter = True
        go = LCRNG.XDRNG(rng.seed)
        # Generated 12 calls after generation
        # go.advance(12)

        tid = 40122
        sid = go.nextUShort()
        txor = tid^sid
        tsv = txor // 8
        high = go.nextUShort()
        low = go.nextUShort()
        
        # Skip Trainer info
        go.advance(3)

        if (0 if low > 7 else 1) != (high ^ 40122 ^ sid):
            high ^= 0x8000

        pxor = high ^ low
        psv = pxor // 8
        shiny = "No"
        if psv == tsv:
            shiny = "Star"
            if pxor == txor:
                shiny = "Square"
        # if shiny != "Star":
        #     filter = False
        #     rng.nextUInt()
        #     continue

        pid = (high << 16) | low
        nature = natures[pid%25]
        # if nature != "Jolly" and nature != "Careful" and nature != "Adamant":
        #     filter = False
        #     rng.nextUInt()
        #     continue
        ivs = [0]*6
        for i in range(6):
            if i == 3:
                i = 5
            elif i > 3:
                i -= 1
            ivs[i] = (go.nextUShort() >> 11)
        # if ivs[0] < 28 or ivs[1] < 28 or ivs[2] < 28 or ivs[4] < 28 or ivs[5] < 28:
        #     filter = False
        #     rng.nextUInt()
        #     continue

        if filter:
            print(f"{advance}, {rng.seed:08X}, {shiny}, {sid:05}, {pid:08X}, {nature}, {str(ivs)}")
    rng.nextUInt()
