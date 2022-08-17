lotto = int(input("lotto: "))
print("Press enter for next lotto")
i = 1
while True:
    lotto = (lotto * 0x8965 + 0xF729) & 0xFFFF
    print(i,lotto,end="")
    input()
    i += 1