# Mersenne Twister Class

class MT:
    def __init__(self, seed = 0):
        self.state = [0]*624
        self.index = 624

        self.state[0] = seed
        for i in range(1,624):
            self.state[i] = (0x6c078965*(self.state[i-1]^(self.state[i-1]>>30)) + i) & 0xFFFFFFFF

    def advance(self, advances):
        advances += index
        while advances >= 624:
            self.shuffle()
            advances -= 624
        index = advances

    def next(self):
        if self.index == 624:
            self.shuffle()
            index = 0

        y = self.state[self.index]
        y ^= (y>>11)
        y ^= ((y<<7)&0x9d2c5680)
        y ^= ((y<<15)&0xefc60000)
        y ^= (y>>18)
        self.index+=1
        return y & 0xFFFFFFFF

    def nextUShort(self):
        return self.next() >> 16
    
    def shuffle(self):
        for i in range(624):
            y = ((self.state[i]&0x80000000) | (self.state[(i+1)%624]&0x7fffffff)) & 0xFFFFFFFF
            y1 = y>>1
            if y%2 != 0:
                y1 ^= 0x9908b0df
            self.state[i] = self.state[(i+397)%624]^y1
        self.index = 0
