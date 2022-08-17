"""
Colosseum blink prediction
"""
from rngs import LCRNG

class BlinkTracker:
    def __init__(self, seed, interval=4):
        self.rng = LCRNG.XDRNG(seed)
        self.counter = 0
        self.interval = interval
        self.break_time = 0
        self.threshold = 0

    def next(self):
        if self.break_time > 0:
            self.break_time -= 1
            return False
        self.counter += 2
        if self.counter < 10:
            return False
        if self.counter < 60:
            self.set_threshold()
        elif self.counter < 180:
            self.threshold = 0.0166667
        else:
            self.threshold = 1
        rand = self.rng.nextFloat()
        if rand <= self.threshold:
            count = self.counter
            self.counter = 0
            self.break_time = self.interval
            return count
        return True

    def set_threshold(self):
        f0 = 0.0166667
        f2 = 50
        f1 = 2
        f3 = self.counter - 10
        f2 = f3 / f2
        f1 = f1 - f2
        f31 = f2 * f1
        f31 = f31 * f0
        self.threshold = f31
    
    def advance(self,advances):
        self.rng.advance(advances)


if __name__ == "__main__":
    seed = int(input("Seed: 0x"),16)
    is_eu = int(input("Non-EU/EU (0/1): "))
    min_adv = int(input("Min Advance: "))
    max_adv = int(input("Max Advance: "))
    tracker = BlinkTracker(seed,interval = 5 if is_eu else 4)
    tracker.advance(min_adv)
    advance = min_adv
    wait_advance = 0
    prev_blink = 0
    blink_interval = []
    print("VFrame\tAdvanceSinceStart\tVFramesSinceLastBlink\tAdvance\tSeed")
    while advance < max_adv-min_adv:
        flag = tracker.next()
        if flag:
            advance += 1
        wait_advance += 1
        if flag is not True:
            if flag is not False:
                current_seed = tracker.rng.seed
                blink = wait_advance
                if prev_blink == 0:
                    prev_blink = blink
                    blink_interval.append(blink)
                else:
                    blink_interval.append(blink - prev_blink)
                print(f"{wait_advance}\t{advance}\t\t\t{blink-prev_blink}\t\t\t{advance + min_adv}\t{current_seed:08X}")
                prev_blink = blink

