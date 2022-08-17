class RNGList:
    def __init__(self,rng,size):
        self.states = []
        self.head = 0
        self.pointer = 0
        self.rng = rng
        self.size = size
        for i in range(self.size):
            self.states.append(self.rng.next())
    
    def advanceStates(self,frames):
        for frame in range(frames):
            self.advanceState()

    def advanceState(self):
        self.head &= self.size - 1
        self.states[self.head] = self.rng.next()
        self.head += 1
        self.pointer = self.head
    
    def advanceFrames(self,frames):
        self.pointer = (self.pointer + frames) & (self.size - 1)
    
    def getValue(self):
        self.pointer &= self.size - 1
        self.pointer += 1
        return self.states[self.pointer-1]
    
    def resetState(self):
        self.pointer = self.head
