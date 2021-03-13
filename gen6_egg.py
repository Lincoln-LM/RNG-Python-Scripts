import MT
import RNGPool

natures = [ "Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky" ]
male_parent = [31,31,31,31,31,31]
female_parent = [31,31,31,31,31,31]


mt = MT.MT(19650218)
mt.reseed_key([0,1],2)
rngList = RNGPool.RNGList(mt,1024)

def rand(n):
    return (rngList.getValue() * n>>32) & 0xFFFFFFFF
def rand2():
    return rngList.getValue() < 0x80000000

rngList.advanceFrames(624)
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
print("EC, IVs, Nature, Gender, Ability")
print(hex(EC),IVs,natures[Nature],Gender,Ability)
