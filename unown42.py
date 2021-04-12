# Gen 4 Unown RNG - Don't fully trust this not updated

import LCRNG
from tools import getIVs

letters = ["A","B","C","D","E","F","G","H","I","J","R","S","T","U","V","K","L","M","N","O","P","Q","W","X","Y","Z","!","?"]
radio_symbols = ["Y","N"]
seen = []
for _ in range(26):
    seen.append(False)

def generate(seed):
    state = []
    seen_go = seen.copy()
    go = LCRNG.PokeRNG(seed)
    low = go.nextUShort()
    high = go.nextUShort()
    pid = (high<<16) | low
    iv1 = go.nextUShort()
    iv2 = go.nextUShort()
    ivs = getIVs(iv1, iv2)
    go.nextUInt()
    letterrand = go.nextUShort()
    main_letter = letters[letterrand%26]
    qe_letter = letters[letterrand%2+26]
    radio = radio_symbols[0] if letterrand%100 < 50 else radio_symbols[1]
    radio_letters = ""
    letterrand = go.nextUShort()
    if radio == radio_symbols[0]:
        for letter_count in range(seen_go.count(False),0,-1):
            letter_value = letterrand%letter_count
            letter_check = 0
            for i in range(26):
                if not seen_go[i]:
                    if letter_value == letter_check:
                        radio_letters += letters[i]
                        seen_go[i] = True
                        break
                    letter_check += 1
    else:
        radio_letters = letters[letterrand%26]
    state.append(hex(pid))
    state += ivs
    state.append(main_letter)
    state.append(qe_letter)
    state.append(radio)
    state.append(radio_letters)

    return state

seed = int(input("Seed: 0x"),16)
seen_letters = input("Type all the seen letters (ex: ABLPTX) press enter if none): ")
for letter in seen_letters:
    seen[letters.index(letter)] = True
starting_advances = int(input("Starting Advances: "))
total_advances = int(input("Total Advances: "))

rng = LCRNG.PokeRNG(seed)
rng.advance(starting_advances)

print("Advance, PID, HP, ATK, DEF, SPA, SPD, SPE, Letter, !?, Radio")
for advance in range(total_advances):
    print(starting_advances+advance,*generate(rng.seed),sep=", ")
    rng.nextUInt()
