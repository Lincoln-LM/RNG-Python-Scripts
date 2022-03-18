from RNGCache import RNGCache
from LCRNG import PokeRNGR
from tools import getIVs

cache = RNGCache()
natures = ["Hardy","Lonely","Brave","Adamant","Naughty","Bold","Docile","Relaxed","Impish","Lax","Timid","Hasty","Serious","Jolly","Naive","Modest","Mild","Quiet","Bashful","Rash","Calm","Gentle","Sassy","Careful","Quirky"]

NO_LEAD = 0
SYNC = 1
CUTE_CHARM = 2

def undo_pid_loop(seed, nature):
    """Undo pid loop to find the seed from before it started"""
    go = PokeRNGR(seed)
    nextRNG = seed >> 16
    nextRNG2 = go.nextHigh()
    testPID = nature - 1
    possible = []
    while (testPID % 25) != nature: # end loop when a pid of the same nature is found
        if (nextRNG % 25) == nature: # seed that gives correct hunt nature found
            possible.append(go.seed)
        testPID = (nextRNG << 16) | nextRNG2
        nextRNG = go.nextHigh()
        nextRNG2 = go.nextHigh()
    return possible

def undo_pid_loop_sync(seed, nature, sync):
    """Undo pid loop when sync is active"""
    go = PokeRNGR(seed)
    nextRNG = seed >> 16
    nextRNG2 = go.nextHigh()
    testPID = nature - 1
    possible = []
    while (testPID % 25) != nature: # end loop when a pid of the same nature is found
        if (nextRNG & 1) == 0 and (sync == nature): # seed that applies synchronize when sync is of the correct nature is found
            possible.append(go.seed)
        elif (nextRNG2 & 1) == 1 and (nextRNG % 25) == nature: # seed that does not apply sync, but gives the correct hunt nature otherwise is found
            possible.append(PokeRNGR(go.seed).next()) # advance seed once due to sync+hunt nature rand calls
        testPID = (nextRNG << 16) | nextRNG2
        nextRNG = go.nextHigh()
        nextRNG2 = go.nextHigh()
    return possible

def undo_bcc_loop(results, seed, pid, left = 4, lead = NO_LEAD, final_passes = False, sync_nature = None):
    """Recursively undo the BCC perfect iv loop to get starting seed"""
    if lead == SYNC:
        possibles = undo_pid_loop_sync(seed, pid % 25, sync_nature) # undo sync specific loop
    elif lead == CUTE_CHARM and left == 4:
        if (pid & 0xFFFF) % 3: # cute charm succeeds and forces the correct spread
            go = PokeRNGR(seed)
            go.next()
            seed = go.next()
            results.append((lead, sync_nature, seed, left))
            return
        else: # cute charm fails but still offsets the rng
            possibles = undo_pid_loop(seed, pid % 25)
    else:
        possibles = undo_pid_loop(seed, pid % 25)
    for possible in possibles:
        go = PokeRNGR(possible)
        iv2 = possible >> 16
        iv1 = go.next() >> 16
        normal_seed = go.next()
        high = normal_seed >> 16
        cute_charm_seed = go.next()
        low = cute_charm_seed >> 16
        pid = (high << 16) | low
        seed = go.next() # get seed for next step in the iv loop
        if 31 not in getIVs(iv1,iv2): # if there is a 31 in this step it cannnot be used
            if left == 1 or final_passes: # only add results if a path can start here
                if lead == CUTE_CHARM:
                    if iv2 % 3 == 0: # cute charm rand offsets what seed is used, if cute charm succeeds the path cannot be used
                        results.append((lead, sync_nature, cute_charm_seed, left))
                else: # if the lead is not cute charm then add it normally
                    results.append((lead, sync_nature, normal_seed, left))
                if left == 1: # if we have undone all 4 loops then stop recursion
                    return
            undo_bcc_loop(results, seed, pid, left = left - 1, lead = lead, final_passes = final_passes, sync_nature = sync_nature)

ivs = [31,31,31,31,31,31] # ivs to search for
print(ivs)
seeds = cache.recoverLower16BitsIV(*ivs)
results = []
for val in seeds:
    rng = PokeRNGR(val)
    high = rng.nextHigh()
    low = rng.nextHigh()
    pid = (high << 16) | low
    seed = rng.next()
    for flag in (False, True):
        if flag:
            pid ^= 0x80008000
            seed ^= 0x80000000
        for lead in (NO_LEAD, SYNC, CUTE_CHARM): # search all lead types
            if lead == SYNC:
                for sync_nature in range(25): # check every sync nature as each step is affected
                    undo_bcc_loop(results, seed, pid, left = 4, lead = lead, final_passes = 31 in ivs, sync_nature=sync_nature)
            else:
                undo_bcc_loop(results, seed, pid, left = 4, lead = lead, final_passes = 31 in ivs)
print([f"{result[2]:08X} {f'{natures[result[1]]} Sync' if result[0] == SYNC else ('Cute Charm' if result[0] else 'No Lead')}" for result in results])
print(len(results), "found")