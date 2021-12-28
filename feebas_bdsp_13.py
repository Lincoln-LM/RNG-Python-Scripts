from LCRNG import MRNGR,ARNG,MRNG
from random import randint

def find(lottos,swarm=None,sphere1=None,sphere2=None,print_=True):
    possible = set()
    while lottos[0] < 0x100000:
        for low in range(0x1000):
            seed_q = (lottos[0]<<0xc)|low
            seed_q = MRNGR(seed_q).next()
            daily_q = seed_q
            if daily_q > 0x80000000:
                daily_q = 0x100000000 - daily_q
            if swarm != None:
                if daily_q%0x1c != swarm:
                    continue
            if sphere1 != None:
                if (daily_q%999)//333 != sphere1:
                    continue
            if sphere2 != None:
                if (daily_q%1000)//200 != sphere2:
                    continue
            flag = True
            temp = ARNG(seed_q).next()
            for lotto in lottos[1:]:
                flag2 = False
                while lotto < 0x100000:
                    test = (MRNG(temp).next()>>0xc)
                    if test == lotto:
                        flag2 = True
                        break
                    lotto += 100000
                if not flag2:
                    flag = False
                temp = ARNG(temp).next()
            if flag:
                possible.add(seed_q)
                if print_:
                    print("Seed Found:",hex(seed_q))
        lottos[0] += 100000
    return possible


def main():
    seed = 0xDEADBEEF
    print(f"Seed: {seed:08x}")
    lottos = []
    temp = seed
    for _ in range(2):
        lottos.append((MRNG(temp).next()>>0xc)%100000)
        temp = ARNG(temp).next()
    print(f"Lottos: {', '.join(str(l) for l in lottos)}")
    find(lottos)


def test(tests):
    for t in range(tests):
        seed = randint(0,0xFFFFFFFF)
        temp = seed
        daily = seed
        if daily > 0x80000000:
            daily = 0x100000000 - daily
        lottos = []
        swarm = daily%0x1c
        sphere1 = (daily%999)//333
        sphere2 = (daily%1000)//200
        print(swarm)
        for _ in range(2):
            lotto = (MRNG(temp).next()>>0xc)%100000
            lottos.append(lotto)
            print(lotto)
            temp = ARNG(temp).next()
        possible = find(lottos,print_=False)
        if not 0 < len(possible) < 2 or max(possible) != seed:
            print(f"Test {t} Fail {seed:08X} {len(possible)}")
            if len(possible) > 1:
                s1 = set()
                s2 = set()
                s3 = set()
                s4 = set()
                for pos in possible:
                    daily = pos
                    if daily > 0x80000000:
                        daily = 0x100000000 - daily
                    s1.add((daily>>24)%0x84)
                    s2.add(((daily>>16)&0xFF)%0x84)
                    s3.add(((daily>>8)&0xFF)%0x84)
                    s4.add((daily&0xFF)%0x84)
                print(len(s1),len(s2),len(s3),len(s4))

        else:
            print(f"Test {t} Successful")
        


if __name__ == "__main__":
    test(100)