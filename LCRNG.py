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
            
class XDRNG:
    def __init__(self, seed):
        self.seed = seed

    def nextUInt(self):
        self.seed = (self.seed * 0x343FD + 0x269EC3) & 0xffffffff
        return self.seed

    def nextUShort(self):
        return self.nextUInt() >> 16

    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()

class XDRNGR:
    def __init__(self, seed):
        self.seed = seed

    def nextUInt(self):
        self.seed = (self.seed * 0xB9B33155 + 0xA170F641) & 0xffffffff
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
        self.seed = (self.seed * 0x6c078965 + 0x1) & 0xffffffff
        return self.seed

    def nextUShort(self):
        return self.nextUInt() >> 16

    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()
        
class MRNG:
    def __init__(self, seed):
        self.seed = seed
    
    def nextUInt(self):
        self.seed = (self.seed * 0x41C64E6D + 0x3039) & 0xffffffff
        return self.seed
    
    def nextUShort(self):
        return self.nextUInt() >> 16
    
    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()
        
class MRNGR:
    def __init__(self, seed):
        self.seed = seed
    
    def nextUInt(self):
        self.seed = (self.seed * 0xEEB9EB65 + 0xFC77A683) & 0xffffffff
        return self.seed
    
    def nextUShort(self):
        return (self.nextUInt() >> 16) & 0x7FFF
    
    def advance(self, advances):
        for _ in range(advances):
            self.nextUInt()
