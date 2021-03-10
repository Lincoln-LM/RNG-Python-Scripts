# Mersenne Twister Class

class MT:
    def __init__(self, seed = 0):
        self.state = [0]*624
        self.index = 624

        self.state[0] = seed
        for i in range(1,624):
            self.state[i] = (0x6c078965*(self.state[i-1]^(self.state[i-1]>>30)) + i) & 0xFFFFFFFF
    
    def reseed_key(self, init_key, key_length):
        self.state = MT(0x12BD6AA).state
        i = 1
        j = 0
        if 624 > key_length:
            mti = 624
        else:
            mti = key_length
        for mti in range(mti, 0, -1):
            self.state[i] = ((self.state[i] ^ ((self.state[i - 1] ^ (self.state[i - 1] >> 30)) * 0x19660D)) + init_key[j] + j) & 0xFFFFFFFF
            i += 1
            j += 1
            if i >= 624:
                self.state[0] = self.state[624-1]
                i = 1
            if j >= key_length:
                j = 0
        for mti in range(623,0,-1):
            self.state[i] = ((self.state[i] ^ ((self.state[i - 1] ^ (self.state[i - 1] >> 30)) * 0x5D588B65)) - i) & 0xFFFFFFFF
            i += 1
            if i >= 624:
                self.state[0] = self.state[624-1]
                i = 1
        self.index = 0
        
        self.state[0] = 0x80000000
        
    def advance(self, advances):
        advances += self.index
        while advances >= 624:
            self.shuffle()
            advances -= 624
        self.index = advances

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
