mt = MT.MT(19650218)
mt.reseed_key(0,0)
rngList = RNGPool.RNGList(mt,128)

def rand(n):
    return (mt.next() * n>>32) & 0xFFFFFFFF
def rand2():
    return mt.next() < 0x80000000

inherit = [0,0,0,0,0,0]

Gender = rand(252)
Nature = rand(25)
Ability = rand(100)
for i in range(3):
    tmp = rand(6)
    inherit[tmp] = rand2()

IVs = []
for j in range(6):
    IVs.append(mt.next()>>27)
EC = mt.next()
print(hex(EC),IVs,Gender,Nature,Ability,inherit)

    