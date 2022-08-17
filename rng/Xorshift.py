class Xorshift:
    def __init__(self, seed0, seed1, seed2, seed3):
        self.seed = [seed0, seed1, seed2, seed3]

    def next(self):
        self.seed[0] ^= (self.seed[0] << 11) & 0xFFFFFFFF
        self.seed[0] ^= self.seed[0] >> 8
        self.seed[0] ^= self.seed[3] ^ (self.seed[3] >> 19)

        self.seed = self.seed[1:4] + [self.seed[0]]

        return self.seed[3]