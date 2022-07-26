"""Script for predicting raffle items (original script by Twisty)"""
from LCRNG import PokeRNG

def tm_search(total_advances, seed):
    """Search next x advances for a tm"""
    rng = PokeRNG(seed)
    for cnt in range(total_advances):
        rand = rng.nextHigh() % 100
        if rand < 4:
            print(cnt, "advancements wins a TM")
    input("Press enter to quit")

def ball_search(total_advances, seed):
    """Search next x advances for a special ball"""
    rng = PokeRNG(seed)
    for cnt in range(total_advances):
        rand = rng.nextHigh() % 100
        if 3 < rand < 40:
            print(cnt, "advancements wins a special ball")
    input("Press enter to quit")

print("Goldenrod Raffle Corner prize finder")
initial_seed = int(input("Enter seed: 0x"), 16)
max_advances = int(input("Enter max number of advancements: "))

chosen_value = None
while chosen_value is None:
    try:
        chosen_value = int(input("Enter 1 for search for TMs, or 2 for special balls: "))
        if chosen_value == 1:
            tm_search(max_advances, initial_seed)
        elif chosen_value == 2:
            ball_search(max_advances, initial_seed)
        else:
            raise ValueError("Invalid choice")
    except ValueError:
        chosen_value = None
        print("Invalid choice")
