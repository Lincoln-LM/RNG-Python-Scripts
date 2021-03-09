# LCRNG Classes

class PokeRNG:
    def __init__(self, seed):
        self.seed = seed

    def nextUInt(self):
        self.seed = (self.seed * 0x41c64e6d + 0x6073) & 0xffffffff
        return self.seed

    def nextUShort(self):
        return self.nextUInt() >> 16

    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()

class PokeRNGR:
    def __init__(self, seed):
        self.seed = seed

    def nextUInt(self):
        self.seed = (self.seed * 0xEEB9EB65 + 0xA3561A1) & 0xffffffff
        return self.seed

    def nextUShort(self):
        return self.nextUInt() >> 16
    
    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()

class ARNG:
    def __init__(self, seed):
        self.seed = seed

    def nextUInt(self):
        self.seed = (self.seed * 1812433253 + 1) & 0xffffffff
        return self.seed

    def nextUShort(self):
        return self.nextUInt() >> 16

    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()
        