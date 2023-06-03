import math

def encode_rail_fence_cipher(string, n):
    rails = [[] for i in range(n)]
    i = 0
    d = 1
    for c in string:
        rails[i].append(c)
        if i + d > (n-1) or i + d < 0:
            d = -d
        i += d
    print(rails)
    return "".join(["".join(l) for l in rails])
    
def decode_rail_fence_cipher(string, n):
    L = (n + (n-2))
    diff = len(string) / L
    rem = len(string) % L
    print(diff, rem, L)
    rails = []
    rails.append(string[:math.ceil(diff):])
    index = math.ceil(diff)
    for i in range(1, (n-1)):
        endP = index + (math.floor(diff) * 2)
        if rem > i:
            endP += 1
        if rem > L/2 + (L/2 - i):
            endP += 1
        rails.append(string[index:endP:])
        index = endP
    rails.append(string[index::])
    print(rails)
    output = ""
    i = 0
    d = 1
    for c in string:
        output += rails[i][0]
        rails[i] = rails[i][1::]
        if i + d > (n-1) or i + d < 0:
            d = -d
        i += d
    return output
