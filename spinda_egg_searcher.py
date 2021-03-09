import LCRNG
from tools import getIVs
from RNGCache import recoverLower16BitsPID

def getInitial(seed):
    advances = 0
    rng = LCRNG.PokeRNGR(seed)
    while (rng.seed > 0xFFFF):
        rng.nextUInt()
        advances += 1
    return [hex(rng.seed), advances]

def generateLower(seed, compatability):
    go = LCRNG.PokeRNG(seed)
    if ((go.nextUShort() * 100) / 0xFFFF) < compatability:
        pid = ((go.nextUShort() % 0xFFFE) + 1) & 0xFFFF
        return pid

def generateUpper(seed, lower, parents):
    go = LCRNG.PokeRNG(seed)

    pid = go.nextUShort()

    go.nextUInt()
    iv1 = go.nextUShort()
    iv2 = go.nextUShort()
    ivs = getIVs(iv1,iv2)

    go.nextUInt()
    inh1 = go.nextUShort()
    inh2 = go.nextUShort()
    inh3 = go.nextUShort()
    inh = [inh1,inh2,inh3]

    par1 = go.nextUShort()
    par2 = go.nextUShort()
    par3 = go.nextUShort()
    par = [par1,par2,par3]

    ivs = setInheritance(ivs, inh, par, parents)
    return ivs

def setInheritance(ivs, inh, par, parents):
    available = [0,1,2,3,4,5]
    for i in range(3):
        stat = available[inh[i] % (6-i)]
        parent = par[i] & 1
        s = stat
        if s == 3:
            s = 5
        elif s > 3:
            s -= 1

        ivs[s] = parents[parent][s]
        
        j = stat
        while j < 5-i:
            available[j] = available[j+1]
            j += 1
    return ivs

ivq = int(input("Include IVs? (0/1): "))
if ivq:
    print("Type ivs in the format X.X.X.X.X.X")
    parentaivs = input("Parent A IVs: ").split(".")
    parentbivs = input("Parent B IVs: ").split(".")
    targetminivs = input("Minimum IVs: ").split(".")
    targetmaxivs = input("Maximum IVs: ").split(".")
    for i in range(6):
        parentaivs[i] = int(parentaivs[i])
        parentbivs[i] = int(parentbivs[i])
        targetminivs[i] = int(targetminivs[i])
        targetmaxivs[i] = int(targetmaxivs[i])
    

egg_pid = int(input("PID: 0x"),16)

pid1_high = ((egg_pid-1 & 0xFFFF) << 16)
pid2_low = (egg_pid >> 16)
if pid1_high != (((egg_pid-1 & 0xFFFF) % 0xFFFE) << 16):
    print("PID is not possible")
    exit(0)

seeds1 = []
seeds2 = []

og_pid_high = pid1_high
og_pid_low = pid2_low

while len(seeds1) == 0:
    origin = recoverLower16BitsPID(pid1_high)
    for seed in origin:
        go = LCRNG.PokeRNGR(seed)
        seed = go.nextUInt()
        seeds1.append(seed)
    if len(seeds1) == 0:
        pid1_high = ((pid1_high) + 0x1) & 0xFFFFFFFF
        if pid1_high == og_pid_high:
            print("PID is not possible")
            exit(0)

while len(seeds2) == 0:
    origin = recoverLower16BitsPID(pid2_low)
    for seed in origin:
        go = LCRNG.PokeRNGR(seed)
        seed = go.nextUInt()
        if ivq:
            ivs = generateUpper(seed,generateLower(seed,70),[parentaivs,parentbivs])
            check = True
            for i in range(6):
                if ivs[i] > targetmaxivs[i] or ivs[i] < targetminivs[i]:
                    check = False
            if check:
                seeds2.append(seed)
                
        else:
            seeds2.append(seed)
    if len(seeds2) == 0:
        pid2_low = (pid2_low + 0x10000) & 0xFFFFFFFF
        if pid2_low == og_pid_low:
            print("PID is not possible")
            exit(0)


print("------------------------------------------------------------------")
print("Step PID:",hex(pid1_high))
print("Pickup PID:",hex(pid2_low))
print("Egg PID:", hex(((pid2_low & 0xFFFF) << 16) | (((pid1_high >> 16) + 1) & 0xFFFF)))
print()
print("The seed for stepping to generate the egg can be any of the below.")
for seed in seeds1:
    print(hex(seed),getInitial(seed))

print()
print("The seed for picking up the egg can be any of the below.")
for seed in seeds2:
    print(hex(seed),getInitial(seed))
    if ivq:
        print(generateUpper(seed,generateLower(seed,70),[parentaivs,parentbivs]))
