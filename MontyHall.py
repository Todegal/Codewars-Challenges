import random

nGames = 10

def MontyHall(shouldChange):
    i = random.randint(0, 2)
    doors = [False] * 3
    doors[i] = True
    print(doors)
    x = random.randint(0, 2)
    isCorrect = doors[x]
    
    if shouldChange:
        return not isCorrect
    else:
        return isCorrect


print(sum([MontyHall(True) for i in range(nGames)]))
