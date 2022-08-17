class Xorshift:
    def __init__(self, state0, state1):
        self.s0 = state0
        self.s1 = state1

    def seed(self):
        return self.s0, self.s1
    
    def state(self):
        return (self.s1 << 64) | self.s0

    def next(self, n=0x100000000):
        t = self.s0 & 0xFFFFFFFF
        s = self.s1 >> 32

        t ^= (t << 11) & 0xFFFFFFFF
        t ^= t >> 8
        t ^= s ^ (s >> 19)

        self.s0 = ((self.s1 & 0xFFFFFFFF) << 32) | (self.s0 >> 32)
        self.s1 = t << 32 | (self.s1 >> 32)

        return (((t % 0xFFFFFFFF) + 0x80000000) & 0xFFFFFFFF) % n