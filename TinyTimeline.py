from TinyMT import TinyMT

class TinyTimeline(TinyMT):
    def __init__(self, initial_state, index, tiny_advancers):
        self.advances = 0
        self.tiny_advancers = tiny_advancers
        for i,tiny_advancer in enumerate(self.tiny_advancers):
            self.tiny_advancers[i][1] = tiny_advancer[1] - 2
        print(self.tiny_advancers)
        self.index = 0
        self.times_cache = []
        super().__init__(state=initial_state)
        self.advance(index-1)

    def generate_times(self):
        # tiny_advancer = [tiny_advance_type*,last_end_advance]
        # *(https://github.com/wwwwwwzx/3DSRNGTool/blob/68883c3be831f4ccb2dcb5aee22d7fcc734b4aae/3DSRNGTool/Gen6/TinyTimeline.cs#L60)
        times = []
        self.advances = self.tiny_advancers[0][1]
        cooldown = self.getCooldown(self.tiny_advancers[0][0])
        times.append([self.advances+2,self.advances+cooldown,self.index,*self.state])
        self.tiny_advancers.append([self.tiny_advancers[0][0],self.advances+cooldown])
        self.tiny_advancers.pop(0)
        self.tiny_advancers = sorted(self.tiny_advancers, key=lambda x:x[1])
        front = self.next() < 0x55555555
        times.append(["-","-",self.index,*self.state])
        if front:
            front_cooldown = self.getCooldown(2)
            self.advances = self.tiny_advancers[0][1]
            self.tiny_advancers[0][1] = self.advances + front_cooldown
            times.append([self.advances+2,self.advances+front_cooldown,self.index,*self.state])
        
        return times
    
    def next_time(self,include_unhittable=False):
        if len(self.times_cache) == 0:
            self.times_cache = self.generate_times()
        time = ["-"]
        while time[0] == "-":
            if len(self.times_cache) == 0:
                self.times_cache = self.generate_times()
            time = self.times_cache[0]
            self.times_cache.pop(0)
        return time


    def nextState(self):
        self.index += 1
        return super().nextState()

    def rand(self,max,advance=True):
        if advance:
            val = self.next()
        else:
            val = self.temper()
        val = ((val * max) >> 32) & 0xFFFFFFFF
        return val
    
    def getCooldown(self,type):
        if type == 1:
            return self.rand(60) * 2 + 124
        if type == 2:
            return 12 if self.next() > 0x55555555 else 20
        if type == 3:
            return self.rand(90) * 2 + 780
        if type == 4:
            return 360 if self.next() % 3 == 0 else 180
        if type == 5:
            return 542 - (self.rand(180) * 2)
        if type == 6:
            return self.rand(240) + 251
        if type == 7:
            return self.rand(10) * 30 + 60