# Tiny Mersenne Twister Class

class TinyMT:
    def __init__(self, seed = 0, state = [0,0,0,0]):
        self.state = state
        if state == [0,0,0,0]:
            for i in range(1,8):
                self.state[i & 3] ^= (0x6c078965 * (self.state[(i - 1) & 3] ^ (self.state[(i - 1) & 3] >> 30)) + i) & 0xFFFFFFFF
        
            for i in range(8):
                self.nextState()
    
    def advance(self, advances):
        for advance in range(advances):
            self.nextState()
    
    def next(self):
        self.nextState()
        return self.temper()
    
    def nextUShort(self):
        return self.next() >> 16
    
    def nextState(self):
        y = self.state[3]
        x = ((self.state[0] & 0x7FFFFFFF) ^ self.state[1] ^ self.state[2]) & 0xFFFFFFFF

        x ^= (x << 1) & 0xFFFFFFFF
        y ^= ((y >> 1) ^ x) & 0xFFFFFFFF

        self.state[0] = self.state[1] & 0xFFFFFFFF
        self.state[1] = (self.state[2] ^ ((y & 1) * 0x8f7011ee)) & 0xFFFFFFFF
        self.state[2] = (x ^ (y << 10) ^ ((y & 1) * 0xfc78ff1f)) & 0xFFFFFFFF
        self.state[3] = y & 0xFFFFFFFF
    
    def temper(self):
        t0 = self.state[3]
        t1 = (self.state[0] + (self.state[2] >> 8)) & 0xFFFFFFFF

        t0 ^= t1
        if t1 & 1:
            t0 ^= 0x3793fdff
        
        return t0
