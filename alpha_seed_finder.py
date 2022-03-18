import z3

natures = ["Hardy","Lonely","Brave","Adamant","Naughty","Bold","Docile","Relaxed","Impish","Lax","Timid","Hasty","Serious","Jolly","Naive","Modest","Mild","Quiet","Bashful","Rash","Calm","Gentle","Sassy","Careful","Quirky"]

class Xoroshiro(object):
    ulongmask = 2 ** 64 - 1
    uintmask = 2 ** 32 - 1

    def __init__(self, seed, seed2 = 0x82A2B175229D6A5B):
            self.seed = [seed, seed2]

    def state(self):
        s0, s1 = self.seed
        return s0 | (s1 << 64)

    @staticmethod
    def rotl(x, k):
        return ((x << k) | (x >> (64 - k))) & Xoroshiro.ulongmask

    def next(self):
        s0, s1 = self.seed
        result = (s0 + s1) & Xoroshiro.ulongmask
        s1 ^= s0
        self.seed = [Xoroshiro.rotl(s0, 24) ^ s1 ^ ((s1 << 16) & Xoroshiro.ulongmask), Xoroshiro.rotl(s1, 37)]
        return result
    
    def previous(self):
        s0, s1 = self.seed
        s1 = Xoroshiro.rotl(s1, 27)
        s0 = (s0 ^ s1 ^ (s1 << 16)) & Xoroshiro.ulongmask
        s0 = Xoroshiro.rotl(s0, 40)
        s1 ^= s0
        self.seed = [s0,s1]
        return (s0 + s1) & Xoroshiro.ulongmask

    def nextuint(self):
        return self.next() & Xoroshiro.uintmask

    @staticmethod
    def getMask(x):
        x -= 1
        for i in range(6):
            x |= x >> (1 << i)
        return x
    
    def rand(self, N = uintmask):
        mask = Xoroshiro.getMask(N)
        res = self.next() & mask
        while res >= N:
            res = self.next() & mask
        return res

    def quickrand1(self,mask): # 0~mask rand(mask + 1)
        return self.next() & mask

    def quickrand2(self,max,mask): # 0~max-1 rand(max)
        res = self.next() & mask
        while res >= max:
            res = self.next() & mask
        return res

def sym_xoroshiro128plus(sym_s0, sym_s1, result):
    sym_r = (sym_s0 + sym_s1) & 0xFFFFFFFFFFFFFFFF  
    condition = (sym_r & 0xFFFFFFFF) == result

    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    return sym_s0, sym_s1, condition

def sym_xoroshiro128plus64bit(sym_s0, sym_s1, result):
    condition = ((sym_s0 + sym_s1) & 0xFFFFFFFFFFFFFFFF) == result

    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    return sym_s0, sym_s1, condition

def sym_xoroshiro128plusadvance(sym_s0, sym_s1):
    s0 = sym_s0
    s1 = sym_s1
    
    s1 ^= s0
    sym_s0 = z3.RotateLeft(s0, 24) ^ s1 ^ (s1 << 16)
    sym_s1 = z3.RotateLeft(s1, 37)

    return sym_s0, sym_s1

def get_models(s):
    result = []
    while s.check() == z3.sat:
        m = s.model()
        print(m)
        result.append(m)
        
        # Constraint that makes current answer invalid
        d = m[0]
        c = d()
        s.add(c != m[d])

    return result

def generate_from_seed(seed,rolls,guaranteed_ivs=0):
    rng = Xoroshiro(seed)
    ec = rng.rand(0xFFFFFFFF)
    sidtid = rng.rand(0xFFFFFFFF)
    for _ in range(rolls):
        pid = rng.rand(0xFFFFFFFF)
        shiny = ((pid >> 16) ^ (sidtid >> 16) ^ (pid & 0xFFFF) ^ (sidtid & 0xFFFF)) < 0x10
        if shiny:
            break
    ivs = [-1,-1,-1,-1,-1,-1]
    for i in range(guaranteed_ivs):
        index = rng.rand(6)
        while ivs[index] != -1:
            index = rng.rand(6)
        ivs[index] = 31
    for i in range(6):
        if ivs[i] == -1:
            ivs[i] = rng.rand(32)
    ability = rng.rand(2) # rand(3) if ha possible?
    gender = rng.rand(252) + 1 # if set gender then dont roll
    nature = rng.rand(25)
    return ec,pid,ivs,ability,gender,nature,shiny

def find_fixed_seeds(ec,pid,rolls):
    solver = z3.Solver()
    start_s0 = z3.BitVecs('start_s0', 64)[0]

    sym_s0 = start_s0
    sym_s1 = 0x82A2B175229D6A5B

    # EC call
    result = ec
    sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
    solver.add(condition)

    # SIDTID call
    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    # Initial PID rolls
    for _ in range(rolls-1):
        sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)

    # PID call
    result = pid
    sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
    solver.add(condition)
        
    models = get_models(solver)
    return [model[start_s0].as_long() for model in models]

def find_generator_seed(fixed_seed):
    solver = z3.Solver()
    start_s0 = z3.BitVecs('start_s0', 64)[0]

    sym_s0 = start_s0
    sym_s1 = 0x82A2B175229D6A5B

    # Blank call
    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    # Fixed Seed call
    result = fixed_seed
    sym_s0, sym_s1, condition = sym_xoroshiro128plus64bit(sym_s0, sym_s1, result)
    solver.add(condition)

    models = get_models(solver)
    return [model[start_s0].as_long() for model in models]

def find_seed(shiny_rolls,ec_0,pid_0,ivs_0,ec_1,pid_1,ivs_1):
    print()
    print(f"Pokemon 1 EC: {ec_0:08X} PID: {pid_0:08X} IVs: {'/'.join(str(iv) for iv in ivs_0)}")
    print()
    print("Finding possible fixed seeds based on Pokemon 1's EC/PID")

    solver = z3.Solver()
    start_s0 = z3.BitVecs('start_s0', 64)[0]

    sym_s0 = start_s0
    sym_s1 = 0x82A2B175229D6A5B

    # EC call
    result = ec_0
    sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
    solver.add(condition)

    # SIDTID call
    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    # Initial PID rolls
    for _ in range(shiny_rolls-1):
        sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    # PID call
    result = pid_0
    sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
    solver.add(condition)
        
    # models = get_models(solver)
    result = []
    while solver.check() == z3.sat:
        m = solver.model()
        test_seed = m[start_s0].as_long()
        print(f"testing: {test_seed:X}")
        _,_,pred_ivs,_,_,_,_ = generate_from_seed(test_seed,shiny_rolls,guaranteed_ivs=3)
        # print(pred_ivs)
        if pred_ivs == ivs_0:
            print(f"test passed: {test_seed:X}")
            break
        print("test not passed")
        result.append(m)
        
        # Constraint that makes current answer invalid
        d = m[0]
        c = d()
        solver.add(c != m[d])

    # return result

    # pid_ec_seeds = find_fixed_seeds(ec,pid,shiny_rolls)
    # print("Possible fixed seeds:")
    # print(", ".join(hex(seed) for seed in pid_ec_seeds))
    # print()
    # print("Narrowing down results based on Pokemon 1's IVs")
    # fixed_seed = None
    # for seed in pid_ec_seeds:
    #     _,_,pred_ivs,_,_,_,_ = generate_from_seed(seed,shiny_rolls,guaranteed_ivs=3)
    #     if ivs == pred_ivs:
    #         print("Fixed seed found:")
    #         fixed_seed = seed
    #         print(hex(fixed_seed))
    #         break
    # if fixed_seed is None:
    #     raise Exception("Could not deduce fixed seed from the provided information")
    # _,_,_,ability,gender,nature,_ = generate_from_seed(seed,shiny_rolls)
    # print()
    # print("Predicted information for Pokemon 1")
    # print(f"Fixed Seed: {seed:X}")
    # print(f"EC: {ec:X} PID: {pid:X}")
    # print(f"Nature: {natures[nature]} Ability: {ability+1} Gender: {gender}")
    # print(ivs)
    # print()
    # print("Finding possible generator seeds based on Pokemon 1's fixed seed")
    # generator_seeds = find_generator_seed(fixed_seed)
    # print("Possible generator seeds:")
    # print(", ".join(hex(seed) for seed in generator_seeds))
    # print()
    # print("Narrowing down results based on Pokemon 2")
    # generator_seed = None
    # for seed in generator_seeds:
    #     group_seed = (seed - 0x82A2B175229D6A5B) & Xoroshiro.ulongmask
    #     rng = Xoroshiro(group_seed)
    #     rng.next()
    #     rng.next()
    #     rng = Xoroshiro(rng.next())
    #     rng = Xoroshiro(rng.next())
    #     rng.next()
    #     fixed_seed = rng.next()
    #     p_ec,p_pid,p_ivs,p_ability,p_gender,p_nature,p_shiny = generate_from_seed(fixed_seed,shiny_rolls,guaranteed_ivs=3)
    #     if p_ec == ec_2 and p_pid == pid_2 and p_ivs == ivs_2:
    #         print("Generator seed found:")
    #         generator_seed = seed
    #         print(hex(generator_seed))
    #         print("Group seed:")
    #         print(hex(group_seed))
    #         break
    # if generator_seed is None:
    #     raise Exception("Could not deduce generator seed from the provided information")
    # print()
    # print("Predicted information for Pokemon 2")
    # print(f"Fixed Seed: {fixed_seed:X}")
    # print(f"EC: {p_ec:X} PID: {p_pid:X}")
    # print(f"Nature: {natures[p_nature]} Ability: {p_ability+1} Gender: {p_gender}")
    # print(p_ivs)
    # print()
    # adv,ec,pid,ivs,ability,gender,nature = generate_next_shiny(group_seed,shiny_rolls,3)
    # print(f"Next Shiny: {adv}",
    #       f"EC: {ec:X} PID: {pid:X}",
    #       f"Nature: {natures[nature]} Ability: {ability} Gender: {gender}",
    #       f"{'/'.join(str(iv) for iv in ivs)}",sep="\n")

def generate_next_shiny(group_seed,rolls,guaranteed_ivs):
    main_rng = Xoroshiro(group_seed)
    # advance once
    main_rng.next() # spawner 0
    main_rng.next() # spawner 1
    main_rng = Xoroshiro(main_rng.next())
    for adv in range(0,40960):
        generator_seed = main_rng.next()
        main_rng.next() # spawner 1's seed, unused
        rng = Xoroshiro(generator_seed)
        rng.next()
        ec,pid,ivs,ability,gender,nature,shiny = \
            generate_from_seed(rng.next(),rolls,guaranteed_ivs)
        if shiny:
            break
        main_rng = Xoroshiro(main_rng.next())
    return adv,ec,pid,ivs,ability,gender,nature

if __name__ == "__main__":
    # shiny_rolls = int(input("Shiny Rolls: "))
    # print("Pokemon 1")
    # ec_0 = int(input("Encryption Constant: 0x"),16)
    # pid_0 = int(input("PID: 0x"),16)
    # ivs_0 = [int(iv) for iv in input("IVs split by '/' (ex. 31/31/31/31/31/31): ").split("/")]
    # print()
    # print("Pokemon 2")
    # ec_1 = int(input("Encryption Constant: 0x"),16)
    # pid_1 = int(input("PID: 0x"),16)
    # ivs_1 = [int(iv) for iv in input("IVs split by '/' (ex. 31/31/31/31/31/31): ").split("/")]
    shiny_rolls = 32
    group_seed = 0x8877665544332211
    group_rng = Xoroshiro(group_seed)
    spawner_rng = Xoroshiro(group_rng.next())
    slot = spawner_rng.next()
    fixed_seed = spawner_rng.next()
    ec_0,pid_0,ivs_0,_,_,_,_ = generate_from_seed(fixed_seed,shiny_rolls,3)
    group_rng.next()
    group_rng = Xoroshiro(group_rng.next())
    spawner_rng = Xoroshiro(group_rng.next())
    slot = spawner_rng.next()
    fixed_seed = spawner_rng.next()
    ec_1,pid_1,ivs_1,_,_,_,_ = generate_from_seed(fixed_seed,shiny_rolls,3)
    find_seed(shiny_rolls,ec_0,pid_0,ivs_0,ec_1,pid_1,ivs_1)