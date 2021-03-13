import MT
import RNGPool

natures = [ "Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky" ]
male_parent = [31,31,31,31,31,31]
female_parent = [31,31,31,31,31,31]
TSV = 0
PID_Rerollcount = 0
shiny_charm = True
masuda_method = True
if shiny_charm:
    PID_Rerollcount += 2
if masuda_method:
    PID_Rerollcount += 6

def seeds_to_state(pid,seed_0,seed_1):
    mt = MT.MT(19650218)
    mt.reseed_key([seed_0,seed_1],2)
    rngList = RNGPool.RNGList(mt,1024)
    def rand(n):
        return (rngList.getValue() * n>>32) & 0xFFFFFFF
    def rand2():
        return rngList.getValue() < 0x80000000
    rngList.advanceFrames(624)
    Shiny = False
    inherit = [None,None,None,None,None,None]
    Gender = rand(252)
    Nature = rand(25)
    Ability = rand(100)
    for i in range(3):
        tmp = rand(6)
        while inherit[tmp] != None:
            tmp = rand(6)
        inherit[tmp] = rand2()
    IVs = []
    for j in range(6):
        IVs.append(rngList.getValue()>>27)
        if inherit[j] != None:
            if inherit[j]:
                IVs[j] = male_parent[j]
            else:
                IVs[j] = female_parent[j]
    EC = rngList.getValue()
    PID = pid
    for i in range(PID_Rerollcount,0,-1):
        PID = rngList.getValue()
        PSV = ((PID >> 16) ^ (PID & 0xFFFF)) >> 4
        if PSV == TSV:
            Shiny = True
            break
    return [hex(PID),hex(EC),IVs,natures[Nature],Gender,Ability,"Shiny" if Shiny else "Not Shiny"]

seed = int(input("Initial Seed: 0x"),16)
starting_frame = int(input("Starting Frame: "))
total_frames = int(input("Total Frames: "))

mt = MT.MT(seed)
rngList = RNGPool.RNGList(mt,128)
rngList.advanceStates(starting_frame+1)


print("PID, EC, IVs, Nature, Gender, Ability, Seeds")
for _ in range(total_frames):
    pid = rngList.getValue()
    seed_0 = rngList.getValue()
    seed_1 = rngList.getValue()
    print(*seeds_to_state(pid,seed_0,seed_1),hex(seed_1)[2:]+hex(seed_0)[2:])
    rngList.advanceState()